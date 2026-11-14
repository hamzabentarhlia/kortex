export function init(form) {
  const msgs = JSON.parse(form.dataset.i18n);
  form.setAttribute('novalidate', '');
  const fields = [...form.querySelectorAll('.field')];
  const pick = (input) => {
    const key = input.name === 'Website' ? 'site' : input.type === 'email' ? 'email' : input.name === 'name' ? 'name' : 'other';
    return input.validity.typeMismatch && input.value ? msgs[key + '_bad'] || msgs[key] : msgs[key];
  };
  fields.forEach((f, i) => {
    const input = f.querySelector('input:not([type=hidden]), textarea');
    const label = f.querySelector('label');
    if (!input || !label) return;
    f.classList.add('fl');
    const sync = () => f.classList.toggle('is-filled', input.value.trim() !== '');
    input.addEventListener('input', sync);
    input.addEventListener('change', sync);
    sync();
    const msg = document.createElement('p');
    msg.className = 'ff-msg';
    msg.id = 'ffm-' + i;
    msg.hidden = true;
    f.append(msg);
    const check = (show) => {
      const bad = input.required || input.value ? !input.checkValidity() : false;
      if (bad && show) {
        msg.textContent = pick(input);
        msg.hidden = false;
        input.setAttribute('aria-invalid', 'true');
        input.setAttribute('aria-describedby', msg.id);
      } else if (!bad) {
        msg.hidden = true;
        input.removeAttribute('aria-invalid');
        input.removeAttribute('aria-describedby');
      }
      return !bad;
    };
    input.addEventListener('blur', () => { if (input.value || f.dataset.touched) check(true); f.dataset.touched = '1'; });
    input.addEventListener('input', () => { if (input.getAttribute('aria-invalid')) check(true); });
    f.__check = check;
  });
  form.addEventListener('submit', (e) => {
    let first = null;
    fields.forEach((f) => {
      if (!f.__check) return;
      if (!f.__check(true) && !first) first = f.querySelector('input, textarea');
    });
    if (first) { e.preventDefault(); e.stopImmediatePropagation(); first.focus(); }
  }, true);
}
