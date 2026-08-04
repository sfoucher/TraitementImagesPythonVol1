import { truncateText, renderMarkdown, buildPayload, MAX_PAGE_CHARS } from './lib.js';

const STYLE = `
  :host { all: initial; }
  .bubble {
    position: fixed; bottom: 20px; right: 20px; width: 56px; height: 56px;
    border-radius: 50%; background: #2b6cb0; color: white; border: none;
    font-size: 24px; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,.3);
    z-index: 999999;
  }
  .tab {
    position: fixed; bottom: 20px; right: 0; padding: 6px 10px;
    background: #2b6cb0; color: white; opacity: .5; font-size: 12px;
    border-radius: 6px 0 0 6px; cursor: pointer; z-index: 999999;
    font-family: sans-serif;
  }
  .tab:hover { opacity: .9; }
  .panel {
    position: fixed; bottom: 88px; right: 20px; width: 340px; max-width: 90vw;
    height: 460px; max-height: 70vh; background: white; border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0,0,0,.3); display: flex; flex-direction: column;
    font-family: sans-serif; font-size: 14px; z-index: 999999; overflow: hidden;
  }
  .header { background: #2b6cb0; color: white; padding: 8px 10px; display: flex;
    align-items: center; justify-content: space-between; gap: 6px; }
  .header select { font-size: 12px; }
  .header button { background: transparent; border: none; color: white; cursor: pointer; font-size: 14px; }
  .messages { flex: 1; overflow-y: auto; padding: 8px; }
  .msg { margin-bottom: 8px; padding: 6px 8px; border-radius: 6px; max-width: 85%; }
  .msg.user { background: #ebf8ff; margin-left: auto; }
  .msg.assistant { background: #f0f0f0; }
  .msg.error { background: #fed7d7; }
  .msg pre { white-space: pre-wrap; background: #1a202c; color: #eee; padding: 6px;
    border-radius: 4px; overflow-x: auto; }
  .inputRow { display: flex; border-top: 1px solid #ddd; }
  .inputRow textarea { flex: 1; border: none; padding: 8px; resize: none; font: inherit; }
  .inputRow button { border: none; background: #2b6cb0; color: white; padding: 0 14px; cursor: pointer; }
  .inputRow button:disabled { background: #a0aec0; cursor: not-allowed; }
  @media (max-width: 480px) {
    .panel { width: 92vw; right: 4vw; }
  }
`;

const STORAGE_ENABLED = 'ia_companion_enabled';
const STORAGE_LEVEL = 'ia_companion_level';
const FETCH_TIMEOUT_MS = 20000;

function getWorkerUrl() {
  const script = document.currentScript || document.querySelector('script[data-worker-url]');
  return script?.dataset.workerUrl;
}

function getPageContext() {
  const el = document.querySelector('#quarto-document-content')
    || document.querySelector('main')
    || document.body;
  return truncateText(el.innerText, MAX_PAGE_CHARS);
}

function isEnabled() {
  return localStorage.getItem(STORAGE_ENABLED) !== 'false';
}

function getLevel() {
  return localStorage.getItem(STORAGE_LEVEL) === 'expert' ? 'expert' : 'beginner';
}

class IaCompanionWidget {
  constructor(root, workerUrl) {
    this.root = root;
    this.workerUrl = workerUrl;
    this.history = [];
    this.cooldownUntil = 0;
    this.render();
  }

  render() {
    this.history = [];
    this.root.innerHTML = '';
    const style = document.createElement('style');
    style.textContent = STYLE;
    this.root.appendChild(style);
    this.panel = null;

    if (!isEnabled()) {
      this.renderTab();
      return;
    }
    this.renderBubble();
  }

  renderTab() {
    const tab = document.createElement('div');
    tab.className = 'tab';
    tab.textContent = "Activer l'assistant IA";
    tab.addEventListener('click', () => {
      localStorage.setItem(STORAGE_ENABLED, 'true');
      this.render();
    });
    this.root.appendChild(tab);
  }

  renderBubble() {
    const bubble = document.createElement('button');
    bubble.className = 'bubble';
    bubble.textContent = '💬';
    bubble.addEventListener('click', () => this.openPanel());
    this.root.appendChild(bubble);
    this.bubble = bubble;
  }

  openPanel() {
    if (this.panel) return;
    this.bubble.remove();

    const panel = document.createElement('div');
    panel.className = 'panel';

    const header = document.createElement('div');
    header.className = 'header';
    const title = document.createElement('span');
    title.textContent = 'Assistant IA';

    const levelSelect = document.createElement('select');
    levelSelect.innerHTML = '<option value="beginner">Débutant</option><option value="expert">Expert</option>';
    levelSelect.value = getLevel();
    levelSelect.addEventListener('change', () => localStorage.setItem(STORAGE_LEVEL, levelSelect.value));

    const minimizeBtn = document.createElement('button');
    minimizeBtn.textContent = '–';
    minimizeBtn.title = 'Réduire';
    minimizeBtn.style.marginRight = '8px';
    minimizeBtn.addEventListener('click', () => {
      this.panel.remove();
      this.panel = null;
      this.messagesEl = null;
      this.renderBubble();
    });

    const disableBtn = document.createElement('button');
    disableBtn.textContent = '✕';
    disableBtn.title = "Désactiver l'assistant";
    disableBtn.addEventListener('click', () => {
      localStorage.setItem(STORAGE_ENABLED, 'false');
      this.render();
    });

    header.append(title, levelSelect, minimizeBtn, disableBtn);

    const messages = document.createElement('div');
    messages.className = 'messages';

    const inputRow = document.createElement('div');
    inputRow.className = 'inputRow';
    const textarea = document.createElement('textarea');
    textarea.rows = 2;
    textarea.placeholder = 'Pose ta question sur cette page...';
    const sendBtn = document.createElement('button');
    sendBtn.textContent = 'Envoyer';
    sendBtn.addEventListener('click', () => this.send(textarea, sendBtn, messages));
    textarea.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.send(textarea, sendBtn, messages);
      }
    });
    // Empêche les touches de fuir vers les raccourcis globaux de Quarto
    // (le retargeting du shadow DOM masque le textarea → Quarto croit qu'aucun
    // champ n'est actif et capture « / », « s »… dans sa barre de recherche).
    ['keydown', 'keyup', 'keypress'].forEach((evt) =>
      textarea.addEventListener(evt, (e) => e.stopPropagation()));

    inputRow.append(textarea, sendBtn);
    panel.append(header, messages, inputRow);
    this.root.appendChild(panel);
    this.panel = panel;
    this.messagesEl = messages;
  }

  addMessage(role, text) {
    const div = document.createElement('div');
    div.className = `msg ${role}`;
    div.innerHTML = role === 'assistant' ? renderMarkdown(text) : text.replace(/</g, '&lt;');
    this.messagesEl.appendChild(div);
    this.messagesEl.scrollTop = this.messagesEl.scrollHeight;
  }

  async send(textarea, sendBtn, messages) {
    if (sendBtn.disabled) return;
    const question = textarea.value.trim();
    if (!question || Date.now() < this.cooldownUntil) return;

    this.addMessage('user', question);
    textarea.value = '';
    sendBtn.disabled = true;

    const payload = buildPayload(question, getPageContext(), getLevel(), this.history);
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);

    try {
      const res = await fetch(this.workerUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });
      clearTimeout(timeout);

      if (res.status === 429) {
        this.cooldownUntil = Date.now() + 30000;
        this.addMessage('error', "Trop de questions d'un coup, réessaie dans 30 secondes.");
        return;
      }
      if (!res.ok) {
        this.addMessage('error', 'Désolé, service indisponible, réessayez.');
        return;
      }
      const data = await res.json();
      this.history.push({ role: 'user', text: question });
      this.history.push({ role: 'assistant', text: data.answer });
      this.addMessage('assistant', data.answer);
    } catch {
      this.addMessage('error', 'Désolé, service indisponible, réessayez.');
    } finally {
      sendBtn.disabled = false;
    }
  }
}

(function init() {
  const workerUrl = getWorkerUrl();
  if (!workerUrl) {
    console.error('ia-companion widget: missing data-worker-url on script tag');
    return;
  }
  const host = document.createElement('div');
  document.body.appendChild(host);
  const shadow = host.attachShadow({ mode: 'open' });
  new IaCompanionWidget(shadow, workerUrl);
})();
