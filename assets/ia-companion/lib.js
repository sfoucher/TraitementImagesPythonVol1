export const MAX_PAGE_CHARS = 45000;

export function truncateText(text, maxChars) {
  if (typeof text !== 'string') return '';
  const trimmed = text.trim();
  return trimmed.length > maxChars ? trimmed.slice(0, maxChars) : trimmed;
}

export function renderMarkdown(text) {
  const escapeHtml = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const NUL = String.fromCharCode(0);
  const PLACEHOLDER_RE = new RegExp(NUL + '(\\d+)' + NUL, 'g');
  const blocks = [];
  const stash = (h) => { blocks.push(h); return NUL + (blocks.length - 1) + NUL; };

  let src = escapeHtml(text);

  // Blocs de code ```lang\n...``` (la ligne de langage est retirée)
  src = src.replace(/```(\w*)\r?\n?([\s\S]*?)```/g, (_, _lang, code) =>
    stash(`<pre><code>${code.replace(/\r?\n$/, '')}</code></pre>`));
  // Code en ligne `...`
  src = src.replace(/`([^`]+)`/g, (_, code) => stash(`<code>${code}</code>`));

  // Éléments en ligne : gras, italique, liens
  const inline = (s) => s
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g,
      '<a href="$2" target="_blank" rel="noopener">$1</a>');

  // Analyse ligne par ligne : titres, listes, paragraphes
  const out = [];
  let list = null;      // { tag: 'ul'|'ol', items: [] }
  let para = [];
  const flushList = () => { if (list) { out.push(`<${list.tag}>${list.items.join('')}</${list.tag}>`); list = null; } };
  const flushPara = () => { if (para.length) { out.push(`<div>${para.join('<br>')}</div>`); para = []; } };

  for (const line of src.split('\n')) {
    if (/^\s*$/.test(line)) { flushPara(); flushList(); continue; }
    const h = line.match(/^(#{1,6})\s+(.*)$/);
    const ul = line.match(/^\s*[-*]\s+(.*)$/);
    const ol = line.match(/^\s*\d+\.\s+(.*)$/);
    if (h) { flushPara(); flushList(); out.push(`<div><strong>${inline(h[2])}</strong></div>`); continue; }
    if (ul) { flushPara(); if (!list || list.tag !== 'ul') { flushList(); list = { tag: 'ul', items: [] }; } list.items.push(`<li>${inline(ul[1])}</li>`); continue; }
    if (ol) { flushPara(); if (!list || list.tag !== 'ol') { flushList(); list = { tag: 'ol', items: [] }; } list.items.push(`<li>${inline(ol[1])}</li>`); continue; }
    flushList();
    para.push(inline(line));
  }
  flushPara(); flushList();

  return out.join('').replace(PLACEHOLDER_RE, (_, i) => blocks[Number(i)]);
}

export function buildPayload(question, pageContext, level, history) {
  return {
    question,
    pageContext: truncateText(pageContext, MAX_PAGE_CHARS),
    level: level === 'expert' ? 'expert' : 'beginner',
    history: history.slice(-6),
  };
}

export function buildQuizPayload(pageContext, level) {
  return {
    mode: 'quiz',
    pageContext: truncateText(pageContext, MAX_PAGE_CHARS),
    level: level === 'expert' ? 'expert' : 'beginner',
  };
}
