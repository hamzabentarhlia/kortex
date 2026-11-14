export function init(root) {
  const data = JSON.parse(root.querySelector('[data-tz-data]').textContent);
  const select = root.querySelector('[data-tz-select]');
  const pane = root.querySelector('[data-tz-pane]');
  const track = (name, props) => { if (window.kxTrack) window.kxTrack(name, props); };
  const el = (tag, cls, text) => {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text) node.textContent = text;
    return node;
  };

  const message = (cls, who) => {
    const box = el('div', 'tz-msg ' + cls);
    box.append(el('span', 'tz-who', who));
    return box;
  };

  select.addEventListener('change', () => {
    const entry = data.entries.find((e) => e.qid === select.value);
    pane.replaceChildren();
    pane.classList.remove('is-skipped');
    if (!entry) return;
    track('teaser_question', { question_id: entry.qid });
    const user = message('tz-user', data.text.you);
    user.append(el('p', '', entry.question));
    const ai = message('tz-ai', data.text.assistant);
    const typed = el('div', 'tz-typed');
    typed.append(el('p', '', entry.summary));
    const sources = el('p');
    sources.append(el('strong', '', data.text.sources + ': '), document.createTextNode(entry.citedTypes.join(', ')));
    typed.append(sources);
    ai.append(typed);
    const caption = el('p', 'tz-caption', data.text.checked.replace('{date}', entry.dateChecked).replace('{engine}', entry.engine));
    const punch = el('p', 'tz-punch', data.punchline);
    const skip = el('button', 'tz-skip', data.text.skip);
    skip.type = 'button';
    skip.addEventListener('click', () => pane.classList.add('is-skipped'));
    pane.append(user, ai, caption, punch, skip);
  });
}
