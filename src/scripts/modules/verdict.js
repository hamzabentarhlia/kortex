export function init(vs) {
  const lang = vs.dataset.lang === 'fr' ? 'fr' : 'en';
  const say = { en: { label: 'Which fits you better', left: 'Other option', mid: 'Both', right: 'KORTEX', both: 'Both fit different needs. Read the two columns side by side.', kortex: 'Choose KORTEX if you want:' }, fr: { label: 'Ce qui vous convient le mieux', left: 'Autre option', mid: 'Les deux', right: 'KORTEX', both: 'Les deux répondent à des besoins différents. Lisez les deux colonnes côte à côte.', kortex: 'Choisissez KORTEX si vous voulez :' } }[lang];
  const cols = [...vs.children].filter((c) => c.tagName === 'DIV');
  if (cols.length < 2) return;
  const better = [...document.querySelectorAll('.prose h2')].find((h) => /better|meilleur|mieux|right call|bon choix/i.test(h.textContent) && !/KORTEX/.test(h.textContent));
  const leftText = better && better.nextElementSibling ? better.nextElementSibling.textContent.trim() : '';
  const leftHead = better ? better.textContent.trim() : cols[0].querySelector('h3').textContent.trim();
  const rightItems = [...cols[cols.length - 1].querySelectorAll('li')].map((li) => li.textContent.trim()).slice(0, 3);
  const bar = document.createElement('div');
  bar.className = 'vd-bar';
  const id = 'vd-' + Math.random().toString(36).slice(2, 7);
  bar.innerHTML = '<label for="' + id + '"></label><input id="' + id + '" type="range" min="0" max="2" step="1" value="1"><div class="vd-ends" aria-hidden="true"><span></span><span></span><span></span></div><p class="vd-out" aria-live="polite"></p>';
  bar.querySelector('label').textContent = say.label;
  const ends = bar.querySelectorAll('.vd-ends span');
  ends[0].textContent = say.left; ends[1].textContent = say.mid; ends[2].textContent = say.right;
  vs.before(bar);
  const input = bar.querySelector('input');
  const out = bar.querySelector('.vd-out');
  const track = (n, p) => { if (window.kxTrack) window.kxTrack(n, p); };
  const set = (fire) => {
    const v = Number(input.value);
    vs.dataset.lean = v === 0 ? 'left' : v === 2 ? 'right' : 'mid';
    input.setAttribute('aria-valuetext', [say.left, say.mid, say.right][v]);
    out.textContent = v === 0 ? leftHead + ' ' + leftText : v === 2 ? say.kortex + ' ' + rightItems.join('; ').toLowerCase() + '.' : say.both;
    if (fire) track('verdict_slide', { lean: vs.dataset.lean, page: location.pathname });
  };
  input.addEventListener('input', () => set(true));
  set(false);
}
