export const MAX_PAGE_CHARS = 45000;

export function truncateText(text, maxChars) {
  if (typeof text !== 'string') return '';
  const trimmed = text.trim();
  return trimmed.length > maxChars ? trimmed.slice(0, maxChars) : trimmed;
}

export function renderMarkdown(text) {
  const escapeHtml = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  let html = escapeHtml(text);

  const NUL = String.fromCharCode(0);
  const PLACEHOLDER_RE = new RegExp(NUL + '(\\d+)' + NUL, 'g');
  const blocks = [];

  function placeholder(i) {
    return NUL + i + NUL;
  }

  html = html.replace(/```([\s\S]*?)```/g, (_, code) => {
    blocks.push(`<pre><code>${code.trim()}</code></pre>`);
    return placeholder(blocks.length - 1);
  });
  html = html.replace(/`([^`]+)`/g, (_, code) => {
    blocks.push(`<code>${code}</code>`);
    return placeholder(blocks.length - 1);
  });

  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  html = html.replace(/\n/g, '<br>');

  html = html.replace(PLACEHOLDER_RE, (_, i) => blocks[Number(i)]);
  return html;
}

export function buildPayload(question, pageContext, level, history) {
  return {
    question,
    pageContext: truncateText(pageContext, MAX_PAGE_CHARS),
    level: level === 'expert' ? 'expert' : 'beginner',
    history: history.slice(-6),
  };
}
