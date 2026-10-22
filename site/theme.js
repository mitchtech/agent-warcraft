// Runs before first paint: apply the saved faction. Horde is dark, Alliance is light, and Horde is the default.
const factionKey = 'agent-warcraft-faction';
const root = document.documentElement;
try {
  if (localStorage.getItem(factionKey) === 'alliance') root.dataset.faction = 'alliance';
} catch {}
root.dataset.pet = root.dataset.faction === 'alliance' ? 'peasant' : 'peon';

document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('#faction-toggle');
  const isAlliance = () => root.dataset.faction === 'alliance';
  const render = () => {
    toggle.setAttribute('aria-pressed', String(isAlliance()));
    document.querySelector('meta[name="theme-color"]').content = getComputedStyle(root).getPropertyValue('--bg').trim();
    document.dispatchEvent(new CustomEvent('factionchange'));
  };
  toggle.addEventListener('click', () => {
    if (isAlliance()) delete root.dataset.faction;
    else root.dataset.faction = 'alliance';
    try { localStorage.setItem(factionKey, isAlliance() ? 'alliance' : 'horde'); } catch {}
    render();
  });
  render();
});
