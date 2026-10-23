/**
 * StudyMate AI — Modern Web Frontend Client
 * B.Tech AI Agent Development Project
 */

// Application State
const state = {
  studentName: localStorage.getItem('studymate_name') || 'Pratik Kamble',
  subject: localStorage.getItem('studymate_subject') || 'AI Agent Development',
  level: localStorage.getItem('studymate_level') || 'Exam-ready',
  apiKey: localStorage.getItem('studymate_api_key') || '',
  theme: localStorage.getItem('studymate_theme') || 'dark',
  soundEnabled: localStorage.getItem('studymate_sound') !== 'false',
  messages: [],
  memory: [],
  isThinking: false
};

// Audio Chime Generator using Web Audio API
class SoundFx {
  constructor() {
    this.ctx = null;
  }
  
  init() {
    if (!this.ctx && (window.AudioContext || window.webkitAudioContext)) {
      this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    }
  }

  playSend() {
    if (!state.soundEnabled) return;
    try {
      this.init();
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(440, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(880, this.ctx.currentTime + 0.12);
      gain.gain.setValueAtTime(0.04, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.12);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.12);
    } catch (_) {}
  }

  playReceive() {
    if (!state.soundEnabled) return;
    try {
      this.init();
      if (!this.ctx) return;
      const now = this.ctx.currentTime;
      const osc1 = this.ctx.createOscillator();
      const osc2 = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      
      osc1.type = 'triangle';
      osc2.type = 'sine';
      osc1.frequency.setValueAtTime(523.25, now); // C5
      osc2.frequency.setValueAtTime(659.25, now + 0.08); // E5
      
      gain.gain.setValueAtTime(0.05, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);
      
      osc1.connect(gain);
      osc2.connect(gain);
      gain.connect(this.ctx.destination);
      
      osc1.start(now);
      osc1.stop(now + 0.09);
      osc2.start(now + 0.08);
      osc2.stop(now + 0.28);
    } catch (_) {}
  }
}

const sfx = new SoundFx();

// DOM Element References
const elements = {
  // Navigation & Profile
  sidebar: document.getElementById('sidebar'),
  openSidebarBtn: document.getElementById('openSidebarBtn'),
  closeSidebarBtn: document.getElementById('closeSidebarBtn'),
  studentNameInput: document.getElementById('studentNameInput'),
  avatarLetter: document.getElementById('avatarLetter'),
  subjectSelect: document.getElementById('subjectSelect'),
  levelTabs: document.getElementById('levelTabs'),
  topSubjectBadge: document.getElementById('topSubjectBadge'),
  topLevelBadge: document.getElementById('topLevelBadge'),
  
  // Tools
  toolCalculatorBtn: document.getElementById('toolCalculatorBtn'),
  toolStudyPlanBtn: document.getElementById('toolStudyPlanBtn'),
  toolQuizBtn: document.getElementById('toolQuizBtn'),
  toolConceptBtn: document.getElementById('toolConceptBtn'),
  
  // Memory
  toggleMemoryBtn: document.getElementById('toggleMemoryBtn'),
  memoryDrawer: document.getElementById('memoryDrawer'),
  memoryCountBadge: document.getElementById('memoryCountBadge'),
  memoryList: document.getElementById('memoryList'),
  memoryEmpty: document.getElementById('memoryEmpty'),
  clearMemoryBtn: document.getElementById('clearMemoryBtn'),
  
  // Engine & Status
  engineDot: document.getElementById('engineDot'),
  engineTitle: document.getElementById('engineTitle'),
  engineSubtitle: document.getElementById('engineSubtitle'),
  
  // Chat Area
  messagesContainer: document.getElementById('messagesContainer'),
  messagesList: document.getElementById('messagesList'),
  heroScreen: document.getElementById('heroScreen'),
  typingIndicator: document.getElementById('typingIndicator'),
  chatForm: document.getElementById('chatForm'),
  messageInput: document.getElementById('messageInput'),
  sendBtn: document.getElementById('sendBtn'),
  clearChatBtn: document.getElementById('clearChatBtn'),
  exportBtn: document.getElementById('exportBtn'),
  themeToggleBtn: document.getElementById('themeToggleBtn'),
  quickCalcBtn: document.getElementById('quickCalcBtn'),
  
  // Calculator Modal
  calcModal: document.getElementById('calcModal'),
  calculatorModalBtn: document.getElementById('calculatorModalBtn'),
  closeCalcModalBtn: document.getElementById('closeCalcModalBtn'),
  calcDisplayExpr: document.getElementById('calcDisplayExpr'),
  calcDisplayResult: document.getElementById('calcDisplayResult'),
  calcEvalBtn: document.getElementById('calcEvalBtn'),
  insertCalcToChatBtn: document.getElementById('insertCalcToChatBtn'),
  copyCalcResultBtn: document.getElementById('copyCalcResultBtn'),
  
  // Settings Modal
  settingsModal: document.getElementById('settingsModal'),
  openSettingsBtn: document.getElementById('openSettingsBtn'),
  closeSettingsModalBtn: document.getElementById('closeSettingsModalBtn'),
  apiKeyInput: document.getElementById('apiKeyInput'),
  testKeyBtn: document.getElementById('testKeyBtn'),
  keyStatusMsg: document.getElementById('keyStatusMsg'),
  soundToggle: document.getElementById('soundToggle'),
  saveSettingsBtn: document.getElementById('saveSettingsBtn'),
  
  toastContainer: document.getElementById('toastContainer')
};

// Configure Markdown Parser
if (window.marked) {
  marked.setOptions({
    gfm: true,
    breaks: true,
    highlight: function(code, lang) {
      if (window.hljs && lang && hljs.getLanguage(lang)) {
        try {
          return hljs.highlight(code, { language: lang }).value;
        } catch (_) {}
      }
      return code;
    }
  });
}

// Show Toast Notification
function showToast(message, duration = 3000) {
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  elements.toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// Initialize Application State & UI
function initApp() {
  // Apply saved theme
  document.documentElement.setAttribute('data-theme', state.theme);
  
  // Initialize Student Info
  elements.studentNameInput.value = state.studentName;
  updateAvatarLetter(state.studentName);
  
  // Subject & Level
  elements.subjectSelect.value = state.subject;
  updateLevelTabs(state.level);
  updateContextBadges();
  
  // Settings UI
  elements.apiKeyInput.value = state.apiKey;
  elements.soundToggle.checked = state.soundEnabled;
  
  // Auto-grow textarea
  setupTextareaAutoGrow();
  
  // Fetch Server Capabilities & Status
  checkServerStatus();
  
  // Load past session messages if available
  const savedMessages = sessionStorage.getItem('studymate_chat');
  if (savedMessages) {
    try {
      state.messages = JSON.parse(savedMessages);
      renderAllMessages();
    } catch (_) {}
  }

  const savedMemory = sessionStorage.getItem('studymate_mem');
  if (savedMemory) {
    try {
      state.memory = JSON.parse(savedMemory);
      renderMemory();
    } catch (_) {}
  }
}

// Update Avatar Initial
function updateAvatarLetter(name) {
  const initial = (name.trim()[0] || 'S').toUpperCase();
  elements.avatarLetter.textContent = initial;
}

// Update Level Tabs UI
function updateLevelTabs(activeLevel) {
  state.level = activeLevel;
  localStorage.setItem('studymate_level', activeLevel);
  const tabs = elements.levelTabs.querySelectorAll('.level-tab');
  tabs.forEach(tab => {
    if (tab.dataset.level === activeLevel) {
      tab.classList.add('active');
    } else {
      tab.classList.remove('active');
    }
  });
  updateContextBadges();
}

// Update Topbar Context Badges
function updateContextBadges() {
  elements.topSubjectBadge.textContent = `📚 ${state.subject}`;
  elements.topLevelBadge.textContent = `🎯 ${state.level}`;
}

// Check Server Engine Status
async function checkServerStatus() {
  try {
    const res = await fetch('/api/status');
    if (!res.ok) throw new Error('Status endpoint unavailable');
    const data = await res.json();
    
    if (data.quota_exhausted) {
      elements.engineDot.className = 'status-indicator-dot';
      elements.engineDot.style.background = '#06b6d4';
      elements.engineDot.style.boxShadow = '0 0 10px #06b6d4';
      elements.engineTitle.textContent = 'Smart Academic Engine';
      elements.engineSubtitle.textContent = 'OpenAI quota $0 • Built-in mode';
    } else if (state.apiKey || data.has_openai_key) {
      elements.engineDot.className = 'status-indicator-dot pulse';
      elements.engineDot.style.background = '#10b981';
      elements.engineDot.style.boxShadow = '0 0 10px #10b981';
      elements.engineTitle.textContent = 'OpenAI AI Connected';
      elements.engineSubtitle.textContent = 'GPT-4o-mini active';
    } else if (data.has_gemini_key) {
      elements.engineDot.className = 'status-indicator-dot pulse';
      elements.engineDot.style.background = '#8b5cf6';
      elements.engineDot.style.boxShadow = '0 0 10px #8b5cf6';
      elements.engineTitle.textContent = 'Google Gemini Free';
      elements.engineSubtitle.textContent = 'Gemini 1.5 Flash active';
    } else {
      elements.engineDot.className = 'status-indicator-dot';
      elements.engineDot.style.background = '#06b6d4';
      elements.engineDot.style.boxShadow = '0 0 10px #06b6d4';
      elements.engineTitle.textContent = 'Smart Academic Engine';
      elements.engineSubtitle.textContent = 'AST & Knowledge Bank Ready';
    }
  } catch (err) {
    elements.engineDot.style.background = '#f59e0b';
    elements.engineTitle.textContent = 'Smart Offline Engine';
    elements.engineSubtitle.textContent = 'Local Mode';
  }
}

// Textarea Auto-expand
function setupTextareaAutoGrow() {
  const tx = elements.messageInput;
  tx.addEventListener('input', () => {
    tx.style.height = 'auto';
    tx.style.height = Math.min(tx.scrollHeight, 140) + 'px';
  });
}

// Render All Messages
function renderAllMessages() {
  if (state.messages.length === 0) {
    elements.heroScreen.style.display = 'flex';
    elements.messagesList.innerHTML = '';
    return;
  }
  
  elements.heroScreen.style.display = 'none';
  elements.messagesList.innerHTML = '';
  state.messages.forEach((msg, idx) => {
    renderMessageNode(msg, idx);
  });
  scrollToBottom();
}

// Render Single Message Bubble
function renderMessageNode(msg, index) {
  const isUser = msg.role === 'user';
  const row = document.createElement('div');
  row.className = `message-row ${isUser ? 'user' : 'assistant'}`;
  
  const avatar = document.createElement('div');
  avatar.className = `msg-avatar ${isUser ? 'user' : 'bot'}`;
  avatar.textContent = isUser ? (state.studentName.trim()[0] || 'U').toUpperCase() : '🎓';

  const wrapper = document.createElement('div');
  wrapper.className = 'message-bubble-wrapper';

  const meta = document.createElement('div');
  meta.className = 'message-meta';
  const timeStr = msg.timestamp || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  
  if (isUser) {
    meta.innerHTML = `<span>${state.studentName}</span> <span>•</span> <span>${timeStr}</span>`;
  } else {
    let modeText = '⚡ Smart Academic Agent';
    if (msg.tool === 'calculator') modeText = '🧮 Safe Calculator';
    else if (msg.tool === 'study_planner') modeText = '📅 Study Planner';
    else if (msg.tool === 'quiz_generator') modeText = '📝 Practice Quiz';
    else if (msg.tool === 'concept_explainer') modeText = '💡 Concept Deep Dive';
    else if (msg.mode === 'openai') modeText = '🤖 GPT-4o-mini';
    else if (msg.mode === 'gemini') modeText = '✨ Gemini Free';
    
    const modeBadge = `<span class="mode-badge ${msg.tool === 'calculator' ? 'calculator' : ''}">${modeText}</span>`;
    meta.innerHTML = `<span>StudyMate</span> <span>•</span> ${modeBadge} <span>•</span> <span>${timeStr}</span>`;
  }

  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';
  
  if (isUser) {
    bubble.textContent = msg.content;
  } else {
    // Markdown rendering for assistant
    if (window.marked) {
      bubble.innerHTML = marked.parse(msg.content);
    } else {
      bubble.textContent = msg.content;
    }
  }

  // Action chips on assistant bubble
  const actionsBar = document.createElement('div');
  actionsBar.className = 'msg-actions';
  
  const copyBtn = document.createElement('button');
  copyBtn.className = 'action-chip';
  copyBtn.innerHTML = `📋 Copy`;
  copyBtn.onclick = () => {
    navigator.clipboard.writeText(msg.content);
    showToast('Message copied to clipboard!');
  };
  actionsBar.appendChild(copyBtn);

  if (!isUser) {
    const memoryBtn = document.createElement('button');
    memoryBtn.className = 'action-chip';
    memoryBtn.innerHTML = `💾 Save to Notes`;
    memoryBtn.onclick = () => {
      addSessionMemory(`Note: ${msg.content.slice(0, 70)}...`);
      showToast('Saved to session memory!');
    };
    actionsBar.appendChild(memoryBtn);
  }

  wrapper.appendChild(meta);
  wrapper.appendChild(bubble);
  wrapper.appendChild(actionsBar);

  if (isUser) {
    row.appendChild(wrapper);
    row.appendChild(avatar);
  } else {
    row.appendChild(avatar);
    row.appendChild(wrapper);
  }

  elements.messagesList.appendChild(row);
}

// Smooth scroll to bottom
function scrollToBottom() {
  elements.messagesContainer.scrollTop = elements.messagesContainer.scrollHeight;
}

// Session Memory Handling
function addSessionMemory(item) {
  if (!state.memory.includes(item)) {
    state.memory.unshift(item);
    if (state.memory.length > 25) state.memory.pop();
    sessionStorage.setItem('studymate_mem', JSON.stringify(state.memory));
    renderMemory();
  }
}

function renderMemory() {
  const count = state.memory.length;
  elements.memoryCountBadge.textContent = `${count} item${count === 1 ? '' : 's'}`;
  
  if (count === 0) {
    elements.memoryEmpty.style.display = 'block';
    elements.memoryList.innerHTML = '';
    return;
  }
  
  elements.memoryEmpty.style.display = 'none';
  elements.memoryList.innerHTML = '';
  state.memory.forEach(item => {
    const li = document.createElement('li');
    li.className = 'memory-item';
    li.textContent = item;
    li.title = item;
    li.onclick = () => {
      elements.messageInput.value = item;
      elements.messageInput.focus();
    };
    elements.memoryList.appendChild(li);
  });
}

// Send Message Flow
async function handleSendMessage(customPrompt = null) {
  const text = (customPrompt || elements.messageInput.value).trim();
  if (!text || state.isThinking) return;

  elements.messageInput.value = '';
  elements.messageInput.style.height = 'auto';

  // Add User Message
  const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  const userMsg = {
    role: 'user',
    content: text,
    timestamp: timeStr
  };

  state.messages.push(userMsg);
  sessionStorage.setItem('studymate_chat', JSON.stringify(state.messages));
  
  addSessionMemory(text);

  // Render & Play Audio
  if (elements.heroScreen.style.display !== 'none') {
    elements.heroScreen.style.display = 'none';
  }
  renderMessageNode(userMsg, state.messages.length - 1);
  sfx.playSend();
  scrollToBottom();

  // Show Thinking State
  state.isThinking = true;
  elements.typingIndicator.style.display = 'flex';
  elements.sendBtn.disabled = true;
  scrollToBottom();

  try {
    const historyPayload = state.messages.slice(-8).map(m => ({
      role: m.role,
      content: m.content
    }));

    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        subject: state.subject,
        level: state.level,
        student_name: state.studentName,
        history: historyPayload,
        api_key: state.apiKey || undefined
      })
    });

    if (!response.ok) {
      throw new Error(`Server returned HTTP ${response.status}`);
    }

    const data = await response.json();
    
    const botMsg = {
      role: 'assistant',
      content: data.reply || 'No response content received.',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      mode: data.mode,
      tool: data.tool_used
    };

    state.messages.push(botMsg);
    sessionStorage.setItem('studymate_chat', JSON.stringify(state.messages));

    elements.typingIndicator.style.display = 'none';
    renderMessageNode(botMsg, state.messages.length - 1);
    sfx.playReceive();
    scrollToBottom();

  } catch (err) {
    elements.typingIndicator.style.display = 'none';
    const errorMsg = {
      role: 'assistant',
      content: `⚠️ **Connection Error:** Could not contact backend server (${err.message}). Make sure \`server.py\` is running.`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      mode: 'error'
    };
    state.messages.push(errorMsg);
    renderMessageNode(errorMsg, state.messages.length - 1);
    scrollToBottom();
  } finally {
    state.isThinking = false;
    elements.sendBtn.disabled = false;
    elements.messageInput.focus();
  }
}

// Calculator Keypad Logic
let calcExpression = '0';
let calcResultVal = '0';

function updateCalcScreen() {
  elements.calcDisplayExpr.textContent = calcExpression;
  elements.calcDisplayResult.textContent = calcResultVal;
}

function handleCalcKey(val) {
  if (val === 'C') {
    calcExpression = '0';
    calcResultVal = '0';
  } else if (val === '=') {
    evaluateCalcExpr();
  } else {
    if (calcExpression === '0' && val !== '.') {
      calcExpression = val;
    } else {
      calcExpression += val;
    }
  }
  updateCalcScreen();
}

async function evaluateCalcExpr() {
  try {
    const res = await fetch('/api/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ expression: calcExpression })
    });
    const data = await res.json();
    if (data.success) {
      calcResultVal = data.result;
    } else {
      calcResultVal = `Error: ${data.error}`;
    }
  } catch (err) {
    calcResultVal = 'Server Error';
  }
  updateCalcScreen();
}

// Export Chat to Markdown File
function exportChatSession() {
  if (state.messages.length === 0) {
    showToast('No messages to export.');
    return;
  }

  let doc = `# StudyMate AI — Academic Study Session\n`;
  doc += `**Student:** ${state.studentName}  \n`;
  doc += `**Subject:** ${state.subject}  \n`;
  doc += `**Target Level:** ${state.level}  \n`;
  doc += `**Date:** ${new Date().toLocaleString()}  \n\n`;
  doc += `---\n\n`;

  state.messages.forEach(msg => {
    const sender = msg.role === 'user' ? state.studentName : 'StudyMate AI';
    doc += `### 💬 ${sender} (${msg.timestamp || ''})\n\n`;
    doc += `${msg.content}\n\n`;
  });

  const blob = new Blob([doc], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `StudyMate_${state.subject.replace(/\s+/g, '_')}_${Date.now()}.md`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast('Session exported to Markdown!');
}

// Event Listeners Registration
function setupEventListeners() {
  // Mobile Sidebar Toggle
  elements.openSidebarBtn.addEventListener('click', () => elements.sidebar.classList.add('open'));
  elements.closeSidebarBtn.addEventListener('click', () => elements.sidebar.classList.remove('open'));

  // Student Name Change
  elements.studentNameInput.addEventListener('change', (e) => {
    state.studentName = e.target.value.trim() || 'Student';
    localStorage.setItem('studymate_name', state.studentName);
    updateAvatarLetter(state.studentName);
    showToast(`Updated name to ${state.studentName}`);
  });

  // Subject Change
  elements.subjectSelect.addEventListener('change', (e) => {
    state.subject = e.target.value;
    localStorage.setItem('studymate_subject', state.subject);
    updateContextBadges();
    showToast(`Subject switched to ${state.subject}`);
  });

  // Level Tabs
  elements.levelTabs.addEventListener('click', (e) => {
    const tab = e.target.closest('.level-tab');
    if (tab) {
      updateLevelTabs(tab.dataset.level);
    }
  });

  // Tool Buttons Quick Actions
  elements.toolCalculatorBtn.addEventListener('click', () => {
    elements.calcModal.classList.add('open');
  });

  elements.toolStudyPlanBtn.addEventListener('click', () => {
    handleSendMessage(`Make a proper day-wise timetable starting from Day 1 basic concepts for ${state.subject}.`);
  });

  elements.toolQuizBtn.addEventListener('click', () => {
    handleSendMessage(`Give me 35 setup questions with answers for ${state.subject}.`);
  });

  elements.toolConceptBtn.addEventListener('click', () => {
    handleSendMessage(`Explain the fundamental concepts and exam tips for ${state.subject}.`);
  });

  // Memory Drawer Toggle
  elements.toggleMemoryBtn.addEventListener('click', () => {
    const isVisible = elements.memoryDrawer.style.display !== 'none';
    elements.memoryDrawer.style.display = isVisible ? 'none' : 'flex';
  });

  elements.clearMemoryBtn.addEventListener('click', () => {
    state.memory = [];
    sessionStorage.removeItem('studymate_mem');
    renderMemory();
    showToast('Session memory cleared');
  });

  // Chat Form & Key Navigation
  elements.chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    handleSendMessage();
  });

  elements.messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  });

  // Prompt Chips
  document.querySelectorAll('.chip-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const template = btn.dataset.template;
      elements.messageInput.value = `${template}${state.subject}`;
      elements.messageInput.focus();
    });
  });

  // Starter Cards in Hero Screen
  document.querySelectorAll('.starter-card').forEach(card => {
    card.addEventListener('click', () => {
      handleSendMessage(card.dataset.prompt);
    });
  });

  // Clear Chat
  elements.clearChatBtn.addEventListener('click', () => {
    if (confirm('Clear entire conversation history for this session?')) {
      state.messages = [];
      sessionStorage.removeItem('studymate_chat');
      renderAllMessages();
      showToast('Conversation cleared');
    }
  });

  // Export Session
  elements.exportBtn.addEventListener('click', exportChatSession);

  // Theme Switcher
  elements.themeToggleBtn.addEventListener('click', () => {
    state.theme = state.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', state.theme);
    localStorage.setItem('studymate_theme', state.theme);
    showToast(`Switched to ${state.theme} mode`);
  });

  // Quick Calculator Shortcut Icon in Input
  elements.quickCalcBtn.addEventListener('click', () => {
    elements.messageInput.value = 'calculate: ';
    elements.messageInput.focus();
  });

  // Calculator Modal Controls
  elements.calculatorModalBtn.addEventListener('click', () => elements.calcModal.classList.add('open'));
  elements.closeCalcModalBtn.addEventListener('click', () => elements.calcModal.classList.remove('open'));
  elements.calcModal.addEventListener('click', (e) => {
    if (e.target === elements.calcModal) elements.calcModal.classList.remove('open');
  });

  document.querySelectorAll('.calc-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const val = btn.dataset.val;
      if (val) handleCalcKey(val);
    });
  });

  elements.calcEvalBtn.addEventListener('click', evaluateCalcExpr);

  elements.insertCalcToChatBtn.addEventListener('click', () => {
    elements.calcModal.classList.remove('open');
    handleSendMessage(`calculate: ${calcExpression}`);
  });

  elements.copyCalcResultBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(calcResultVal);
    showToast(`Copied result: ${calcResultVal}`);
  });

  // Settings Modal Controls
  elements.openSettingsBtn.addEventListener('click', () => elements.settingsModal.classList.add('open'));
  elements.closeSettingsModalBtn.addEventListener('click', () => elements.settingsModal.classList.remove('open'));
  elements.settingsModal.addEventListener('click', (e) => {
    if (e.target === elements.settingsModal) elements.settingsModal.classList.remove('open');
  });

  // Test API Key
  elements.testKeyBtn.addEventListener('click', async () => {
    const key = elements.apiKeyInput.value.trim();
    if (!key) {
      elements.keyStatusMsg.className = 'key-status-msg error';
      elements.keyStatusMsg.textContent = 'Please enter an API key first.';
      return;
    }
    const provider = key.startsWith('AIza') ? 'gemini' : 'openai';
    elements.keyStatusMsg.className = 'key-status-msg';
    elements.keyStatusMsg.textContent = `Testing ${provider.toUpperCase()} connection...`;

    try {
      const res = await fetch('/api/validate-key', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api_key: key, provider: provider })
      });
      const data = await res.json();
      if (data.valid) {
        if (data.quota_exhausted) {
          elements.keyStatusMsg.className = 'key-status-msg';
          elements.keyStatusMsg.style.color = '#f59e0b';
          elements.keyStatusMsg.textContent = 'ℹ️ ' + data.message;
        } else {
          elements.keyStatusMsg.className = 'key-status-msg success';
          elements.keyStatusMsg.textContent = '✓ ' + data.message;
        }
      } else {
        elements.keyStatusMsg.className = 'key-status-msg error';
        elements.keyStatusMsg.textContent = '✕ ' + data.message;
      }
    } catch (err) {
      elements.keyStatusMsg.className = 'key-status-msg error';
      elements.keyStatusMsg.textContent = '✕ Could not reach server.';
    }
  });

  // Save Settings
  elements.saveSettingsBtn.addEventListener('click', () => {
    state.apiKey = elements.apiKeyInput.value.trim();
    state.soundEnabled = elements.soundToggle.checked;
    localStorage.setItem('studymate_api_key', state.apiKey);
    localStorage.setItem('studymate_sound', state.soundEnabled);
    elements.settingsModal.classList.remove('open');
    checkServerStatus();
    showToast('Settings saved successfully!');
  });
}

// Start Application on Load
document.addEventListener('DOMContentLoaded', () => {
  initApp();
  setupEventListeners();
});
