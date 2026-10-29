const canvas = document.querySelector('#scope');
const ctx = canvas.getContext('2d');
const panel = canvas.closest('.portrait-panel');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const status = document.querySelector('#audio-status');
const readout = {
  line: document.querySelector('#readout-line'),
  event: document.querySelector('#readout-event'),
  length: document.querySelector('#readout-length'),
};
const alliance = () => document.documentElement.dataset.faction === 'alliance';
const player = new Audio();
player.preload = 'auto';
let audioContext;
let analyzer;
let samples;
let activeButton;
let raf = 0;

// Codex v2 atlas rows: [row, frames, label, first column].
const STATES = {
  idle: [0, 6, 'idle'], 'moving-right': [1, 8, 'moving right'], 'moving-left': [2, 8, 'moving left'], waving: [3, 4, 'waving'],
  jumping: [4, 5, 'jumping'], failure: [5, 8, 'blocked'], waiting: [6, 6, 'waiting for input'], working: [7, 6, 'working'], review: [8, 6, 'reviewing'],
};
const LOOKS = ['up', 'up-right 1', 'up-right 2', 'up-right 3', 'right', 'down-right 1', 'down-right 2', 'down-right 3',
  'down', 'down-left 1', 'down-left 2', 'down-left 3', 'left', 'up-left 1', 'up-left 2', 'up-left 3'];
LOOKS.forEach((name, direction) => { STATES[`look-${direction}`] = [9 + Math.floor(direction / 8), 1, `looking ${name}`, direction % 8]; });
// Which animation the portrait acts out for each cue, mirroring the state Codex would show.
const MOODS = {
  session_started: 'waving', prompt_submitted: 'working', annoyed: 'failure', approval_required: 'waiting', input_required: 'waiting',
  ready_for_input: 'waving', turn_completed: 'jumping', out_of_gold: 'failure', gold_low: 'review', out_of_lumber: 'failure', out_of_food: 'review',
  error: 'failure',
  tool_failed: 'failure', subagent_started: 'moving-right', context_compacting: 'review', session_ended: 'moving-left', 'easter-egg': 'jumping',
};
const mood = event => (event.includes('destructive') ? 'failure' : MOODS[event.split(' ')[0]] || 'idle');

function animator(element) {
  let timer;
  let state = 'idle';
  let paused = false;
  const scale = () => parseFloat(getComputedStyle(element).getPropertyValue('--scale')) || 1;
  const draw = (row, column) => { element.style.backgroundPosition = `${-column * 192 * scale()}px ${-row * 208 * scale()}px`; };
  const render = () => {
    clearInterval(timer);
    const [row, count, , start = 0] = STATES[state];
    let frame = 0;
    draw(row, start);
    if (paused || reducedMotion.matches || document.hidden || count < 2) return;
    timer = setInterval(() => { frame = (frame + 1) % count; draw(row, frame); }, 160);
  };
  return {
    set(next) { state = next; render(); },
    pause(value) { paused = value; render(); },
    get paused() { return paused; },
    render,
  };
}

const portraitPet = animator(document.querySelector('#portrait-sprite'));
const stagePet = animator(document.querySelector('#stage-sprite'));
reducedMotion.addEventListener('change', () => { portraitPet.render(); stagePet.render(); });
document.addEventListener('visibilitychange', () => { portraitPet.render(); stagePet.render(); });
new ResizeObserver(() => { portraitPet.render(); stagePet.render(); }).observe(document.body);

// The portrait is dark in both factions, so only the trace color follows the faction.
const trace = () => (alliance() ? '#6fb0ff' : '#8fd14f');

function fit() {
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  const { width, height } = canvas.getBoundingClientRect();
  canvas.width = Math.round(width * ratio);
  canvas.height = Math.round(height * ratio);
}

function backdrop(fade = 1) {
  const { width, height } = canvas;
  ctx.fillStyle = `rgba(5, 8, 6, ${fade})`;
  ctx.fillRect(0, 0, width, height);
  // A vignette and faint rings suggest a unit portrait without depicting one.
  const vignette = ctx.createRadialGradient(width / 2, height / 2, height * 0.1, width / 2, height / 2, height * 0.8);
  vignette.addColorStop(0, 'rgba(255, 255, 255, 0.03)');
  vignette.addColorStop(1, 'rgba(0, 0, 0, 0.5)');
  ctx.fillStyle = vignette;
  ctx.fillRect(0, 0, width, height);
  ctx.strokeStyle = 'rgba(201, 162, 74, 0.12)';
  ctx.lineWidth = 1;
  for (let r = 1; r <= 3; r++) {
    ctx.beginPath();
    ctx.arc(width / 2, height / 2, (height * r) / 7, 0, Math.PI * 2);
    ctx.stroke();
  }
}

function stroke(points, gain = 1) {
  const { width, height } = canvas;
  const color = trace();
  ctx.save();
  ctx.strokeStyle = color;
  ctx.lineWidth = Math.max(2, width / 260);
  ctx.lineJoin = 'round';
  ctx.shadowColor = color;
  ctx.shadowBlur = width / 40;
  ctx.beginPath();
  points.forEach((value, index) => {
    const x = (index / (points.length - 1)) * width;
    const y = height / 2 - Math.max(-1, Math.min(1, value * gain)) * height * 0.4;
    if (index) ctx.lineTo(x, y); else ctx.moveTo(x, y);
  });
  ctx.stroke();
  ctx.restore();
}

function idle() {
  cancelAnimationFrame(raf);
  backdrop();
  // A slow breath on the standby trace, fixed rather than animated.
  stroke(Array.from({ length: 200 }, (_, i) => Math.sin(i * 0.07) * 0.02 + Math.sin(i * 0.9) * 0.004));
}

function live() {
  analyzer.getFloatTimeDomainData(samples);
  backdrop(0.35);
  // Speech rarely peaks past a third of full scale, so the live trace is amplified to fill the portrait.
  stroke(samples, 2.6);
  raf = requestAnimationFrame(live);
}

// Reduced motion: draw the whole clip's amplitude envelope once instead of animating.
async function envelope(url) {
  const buffer = await audioContext.decodeAudioData(await (await fetch(url)).arrayBuffer());
  const channel = buffer.getChannelData(0);
  const columns = 200;
  const step = Math.floor(channel.length / columns) || 1;
  const peaks = Array.from({ length: columns }, (_, column) => {
    let peak = 0;
    for (let i = column * step; i < (column + 1) * step && i < channel.length; i++) peak = Math.max(peak, Math.abs(channel[i]));
    return peak;
  });
  idle();
  stroke(peaks.flatMap(peak => [peak, -peak]));
}

function ensureAudio() {
  if (audioContext) return audioContext.resume();
  audioContext = new AudioContext();
  analyzer = audioContext.createAnalyser();
  analyzer.fftSize = 2048;
  samples = new Float32Array(analyzer.fftSize);
  audioContext.createMediaElementSource(player).connect(analyzer);
  analyzer.connect(audioContext.destination);
  return audioContext.resume();
}

// Demo economy: each preview costs gold, the mine refills slowly, and an empty treasury gets the advisor's line.
const COST = 15;
const gold = { value: 300, max: 300, node: document.querySelector('#gold') };
const lumber = { value: 0, node: document.querySelector('#lumber') };
setInterval(() => {
  if (gold.value < gold.max) { gold.value = Math.min(gold.max, gold.value + 5); gold.node.textContent = gold.value; }
}, 1000);
const BROKE = {
  horde: { clip: 'orc-need-more-gold', line: 'We need more gold!', length: '1.37' },
  alliance: { clip: 'human-more-gold', line: 'More gold is required.', length: '1.31' },
};

function spend() {
  const chip = gold.node.parentElement;
  if (gold.value < COST) {
    chip.classList.remove('broke');
    void chip.offsetWidth;
    chip.classList.add('broke');
    return false;
  }
  gold.value -= COST;
  gold.node.textContent = gold.value;
  lumber.node.textContent = ++lumber.value;
  chip.dataset.delta = `-${COST}`;
  chip.classList.remove('spent');
  void chip.offsetWidth;
  chip.classList.add('spent');
  return true;
}

function settle(message) {
  panel.classList.remove('live', 'pissed');
  portraitPet.set('idle');
  activeButton?.classList.remove('playing');
  activeButton = null;
  if (!reducedMotion.matches) idle();
  if (message) status.textContent = message;
}

async function play(source, { free = false } = {}) {
  let { clip, line, event, length } = source.dataset || source;
  if (!free && !spend()) {
    ({ clip, line, length } = BROKE[alliance() ? 'alliance' : 'horde']);
    event = 'out_of_gold · the demo treasury is empty';
  }
  const button = source instanceof HTMLElement ? source : null;
  activeButton?.classList.remove('playing');
  activeButton = button;
  readout.line.textContent = line;
  readout.event.textContent = event;
  readout.length.textContent = `${length} s`;
  const url = `audio/${clip}.wav`;
  try {
    await ensureAudio();
    player.src = url;
    await player.play();
    if (activeButton !== button) return;
    button?.classList.add('playing');
    panel.classList.add('live');
    portraitPet.set(mood(event));
    status.textContent = `Playing: ${line}`;
    cancelAnimationFrame(raf);
    if (reducedMotion.matches) await envelope(url);
    else live();
  } catch {
    if (activeButton === button) settle('Playback unavailable. Check your browser audio settings or try agent-warcraft preview.');
  }
}

player.addEventListener('ended', () => settle('Preview finished. Something need doing? Pick another line.'));
document.querySelectorAll('[data-clip]').forEach(button => button.addEventListener('click', () => play(button)));

// The portrait answers like a WC3 unit: the third click inside ten seconds gets the annoyed lines.
const LINES = {
  horde: {
    what: [['orc-what-you-want', 'What you want?', '0.78'], ['orc-yes', 'Yes?', '0.56'], ['orc-hmm', 'Hmmm?', '0.43'], ['orc-something-need-doing', 'Something need doing?', '1.13']],
    pissed: [['orc-whaaat', 'Whaaat?', '0.90'], ['orc-me-busy', 'Me busy. Leave me alone!', '1.98'], ['orc-no-time-for-play', 'No time for play.', '1.14'], ['orc-not-that-kind-of-orc', 'Me not that kind of orc!', '1.69']],
  },
  alliance: {
    what: [['human-yes-milord', 'Yes, milord?', '0.96'], ['human-what', 'What?', '0.26'], ['human-more-work', 'More work?', '0.77']],
    pissed: [['human-didnt-vote', "You're the king? Well, I didn't vote for you.", '3.34'], ['human-witch', 'We found a witch! May we burn her?', '2.58'], ['human-repressed', "Help! Help! I'm being repressed!", '2.54'], ['human-horse-kicked', 'A horse kicked me once. It hurt.', '3.05']],
  },
};
const clicks = [];
let pissedIndex = 0;
document.querySelector('#portrait').addEventListener('click', () => {
  const now = Date.now();
  clicks.push(now);
  while (clicks.length && now - clicks[0] > 10000) clicks.shift();
  const set = LINES[alliance() ? 'alliance' : 'horde'];
  const annoyed = clicks.length >= 3;
  const [clip, line, length] = annoyed ? set.pissed[pissedIndex++ % set.pissed.length] : set.what[Math.floor(Math.random() * set.what.length)];
  play({ clip, line, length, event: annoyed ? 'annoyed · third click inside 10 s' : 'ready_for_input' }, { free: true }).then(() => {
    if (annoyed) panel.classList.add('pissed');
  });
});

// Command card: twelve hotkeys, voiced by whichever faction is selected.
const CARD = [
  ['R', 'Ready', 'session_started', ['orc-ready', 'Ready to work.', '0.84'], ['human-ready', 'Ready to work.', '1.05']],
  ['W', 'Work', 'prompt_submitted', ['orc-work-work', 'Work, work.', '0.86'], ['human-righto', 'Right-o.', '0.76']],
  ['O', 'Okay', 'prompt_submitted', ['orc-okie-dokie', 'Okey dokey.', '1.01'], ['human-off-i-go', 'Off I go, then!', '0.99']],
  ['S', 'Idle', 'ready_for_input', ['orc-something-need-doing', 'Something need doing?', '1.13'], ['human-more-work', 'More work?', '0.77']],
  ['C', 'Complete', 'turn_completed', ['orc-work-complete', 'Work complete!', '0.88'], ['human-jobs-done', "Job's done!", '0.67']],
  ['G', 'Gold', 'out_of_gold', ['orc-need-more-gold', 'We need more gold!', '1.37'], ['human-more-gold', 'More gold is required.', '1.31']],
  ['L', 'Lumber', 'out_of_lumber', ['orc-need-more-lumber', 'We need more lumber.', '1.47'], ['human-more-lumber', 'More lumber is required.', '1.59']],
  ['A', 'Attack', 'approval_required · destructive', ['orc-under-attack', "We're under attack!", '1.34'], ['human-forces-under-attack', 'Our forces are under attack!', '1.56']],
  ['Z', 'Subagent', 'subagent_started', ['orc-zug-zug', 'Zug zug.', '0.51'], ['human-aye-my-lord', 'Aye, my lord.', '0.81']],
  ['I', 'Compact', 'context_compacting', ['orc-inventory-full', 'Inventory is full.', '1.41'], ['human-inventory-full', 'Inventory is full.', '1.28']],
  ['B', 'Failed', 'tool_failed', ['orc-cant-build-there', "Can't build there.", '1.07'], ['human-cant-build-there', "I can't build there.", '0.86']],
  ['H', 'Rally', 'easter-egg', ['orc-for-the-horde', 'For the Horde!', '1.53'], ['human-for-lordaeron', 'For Lordaeron!', '1.62']],
];
const card = document.querySelector('#command-card');
const hotkeys = new Map();
function renderCard() {
  card.replaceChildren(...CARD.map(([key, label, event, horde, human]) => {
    const [clip, line, length] = alliance() ? human : horde;
    const button = document.createElement('button');
    button.className = 'cmd';
    Object.assign(button.dataset, { clip, line, event, length });
    button.setAttribute('aria-label', `${line} (${event}), hotkey ${key}`);
    button.setAttribute('aria-keyshortcuts', key);
    button.innerHTML = `<b aria-hidden="true">${key}</b><span aria-hidden="true">${label}</span>`;
    button.addEventListener('click', () => play(button));
    hotkeys.set(key.toLowerCase(), button);
    return button;
  }));
}
renderCard();
document.addEventListener('factionchange', () => { renderCard(); if (!panel.classList.contains('live')) idle(); });
document.addEventListener('keydown', event => {
  if (event.metaKey || event.ctrlKey || event.altKey || event.repeat) return;
  if (event.target instanceof Element && event.target.closest('input, textarea, select, [contenteditable]')) return;
  const button = hotkeys.get(event.key.toLowerCase());
  if (!button) return;
  event.preventDefault();
  button.focus({ preventScroll: true });
  play(button);
});

new ResizeObserver(() => { fit(); if (!panel.classList.contains('live')) idle(); }).observe(canvas);
fit();
idle();

// Pet stage: every animation row and look direction in either bundled atlas.
const PETS = {
  peon: ['Peon', 'The Peon, a hunched green orc laborer with a pickaxe, tusks, and a black topknot'],
  peasant: ['Peasant', 'The Peasant, a bearded human worker in a blue hood with a pickaxe'],
};
const stageSprite = document.querySelector('#stage-sprite');
const stateLabel = document.querySelector('#state-label');
let stageState = 'idle';
const petName = () => PETS[document.documentElement.dataset.pet === 'peasant' ? 'peasant' : 'peon'];
function choosePet(id) {
  document.documentElement.dataset.pet = id;
  document.querySelectorAll('[data-pet-choice]').forEach(item => item.setAttribute('aria-pressed', String(item.dataset.petChoice === id)));
  stageSprite.setAttribute('aria-label', PETS[id][1]);
  stateLabel.textContent = `The ${PETS[id][0]} is ${STATES[stageState][2]}`;
}
document.querySelectorAll('[data-pet-choice]').forEach(button => button.addEventListener('click', () => choosePet(button.dataset.petChoice)));
// Switching factions brings that faction's worker to the stage; the pet buttons can still pick either.
document.addEventListener('factionchange', () => choosePet(alliance() ? 'peasant' : 'peon'));
const motionButton = document.querySelector('#motion-toggle');
function renderMotion() {
  motionButton.disabled = reducedMotion.matches;
  motionButton.textContent = reducedMotion.matches ? 'Reduced motion is on' : stagePet.paused ? 'Resume animation' : 'Pause animation';
  motionButton.setAttribute('aria-pressed', String(stagePet.paused || reducedMotion.matches));
}
document.querySelectorAll('[data-state]').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('[data-state]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  stageState = button.dataset.state;
  stagePet.set(stageState);
  stateLabel.textContent = `The ${petName()[0]} is ${STATES[stageState][2]}`;
}));
motionButton.addEventListener('click', () => { stagePet.pause(!stagePet.paused); renderMotion(); });
reducedMotion.addEventListener('change', renderMotion);
renderMotion();
stagePet.set('idle');
portraitPet.set('idle');

document.querySelectorAll('[data-install]').forEach(button => button.addEventListener('click', () => {
  const choice = button.dataset.install;
  document.querySelectorAll('[data-install]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  document.querySelector('#sounds-install').hidden = choice === 'pet';
  document.querySelector('#pet-install').hidden = choice === 'sounds';
}));

document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
  const copyStatus = document.querySelector('#copy-status');
  try {
    // innerText skips the hidden pet's variant of a command.
    await navigator.clipboard.writeText(document.getElementById(button.dataset.copy).innerText);
    copyStatus.textContent = 'Commands copied.';
    button.textContent = 'Copied';
    button.classList.add('copied');
    setTimeout(() => { button.textContent = 'Copy'; button.classList.remove('copied'); }, 2000);
  } catch { copyStatus.textContent = 'Clipboard unavailable. Select and copy the commands above.'; }
}));
