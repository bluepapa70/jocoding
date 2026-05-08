/* ── 역대 출현 횟수 (lottolyzer.com, 2002.12 ~ 2026.05) ── */
const FREQ = {
   1:131,  2:114,  3:131,  4:119,  5:117,
   6:130,  7:132,  8:125,  9:108, 10:129,
  11:129, 12:147, 13:143, 14:133, 15:136,
  16:133, 17:132, 18:135, 19:127, 20:132,
  21:130, 22:117, 23:115, 24:130, 25:111,
  26:127, 27:141, 28:125, 29:122, 30:123,
  31:128, 32:113, 33:137, 34:144, 35:124,
  36:121, 37:124, 38:142, 39:128, 40:128,
  41:119, 42:116, 43:129, 44:125, 45:140
};

const GAMES = 5;
const MAX_FREQ = Math.max(...Object.values(FREQ));

/* 번호 → 볼 색상 */
function ballColor(n) {
  if (n <= 10) return 'y';
  if (n <= 20) return 'b';
  if (n <= 30) return 'r';
  if (n <= 40) return 's';
  return 'g';
}

/* 순위 (빈도 내림차순) */
const BY_FREQ = Object.keys(FREQ).map(Number).sort((a, b) => FREQ[b] - FREQ[a]);
function rankOf(n) { return BY_FREQ.indexOf(n) + 1; }

/* ── 뽑기 알고리즘 ── */
function pickWeighted() {
  const nums = Object.keys(FREQ).map(Number);
  const weights = nums.map(n => FREQ[n]);
  const total = weights.reduce((a, b) => a + b, 0);
  const picked = new Set();
  let tries = 0;
  while (picked.size < 6 && tries++ < 1000) {
    let r = Math.random() * total;
    for (let i = 0; i < nums.length; i++) {
      r -= weights[i];
      if (r <= 0 && !picked.has(nums[i])) { picked.add(nums[i]); break; }
    }
  }
  return [...picked].sort((a, b) => a - b);
}

function pickRandom() {
  const pool = Array.from({ length: 45 }, (_, i) => i + 1);
  for (let i = pool.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [pool[i], pool[j]] = [pool[j], pool[i]];
  }
  return pool.slice(0, 6).sort((a, b) => a - b);
}

/* Top N 고정 + 나머지 빈도수 기반 */
function pickTopN(n) {
  const fixed = BY_FREQ.slice(0, n);
  const fixedSet = new Set(fixed);
  const remaining = Object.keys(FREQ).map(Number).filter(x => !fixedSet.has(x));
  const weights = remaining.map(x => FREQ[x]);
  const total = weights.reduce((a, b) => a + b, 0);

  const extra = new Set();
  let tries = 0;
  while (extra.size < 6 - n && tries++ < 1000) {
    let r = Math.random() * total;
    for (let i = 0; i < remaining.length; i++) {
      r -= weights[i];
      if (r <= 0 && !extra.has(remaining[i])) { extra.add(remaining[i]); break; }
    }
  }
  return [...fixed, ...extra].sort((a, b) => a - b);
}

/* ── 상태 ── */
let mode = 'freq';
let topN = 3;
let lastPicked = [];
let statsOpen = false;
let statSort = 'freq';

function setMode(m) {
  mode = m;
  ['Freq','Random','TopN'].forEach(k => {
    document.getElementById('btn' + k).classList.toggle('active', m === k.toLowerCase());
  });
  document.getElementById('topnWrap').classList.toggle('visible', m === 'topn');
  clearBoard();
}

function setTopN(n) {
  topN = n;
  document.getElementById('topnLabelNum').textContent = n;
  document.querySelectorAll('.topn-btn').forEach((btn, i) => {
    btn.classList.toggle('active', i + 1 === n);
  });
  clearBoard();
}

/* ── 생성 ── */
function generate() {
  const board = document.getElementById('board');
  board.innerHTML = '';
  lastPicked = [];

  const fixedNums = mode === 'topn' ? new Set(BY_FREQ.slice(0, topN)) : new Set();

  for (let g = 0; g < GAMES; g++) {
    const nums = mode === 'freq'   ? pickWeighted()
               : mode === 'random' ? pickRandom()
               : mode === 'topn'   ? pickTopN(topN)
               :                     pickWeighted();

    lastPicked.push(...nums);

    const row = document.createElement('div');
    row.className = 'game-row';

    const ballsHTML = nums.map(n => {
      const rank = rankOf(n);
      const isFixed = mode === 'topn' && fixedNums.has(n);
      const isHot = rank <= 5;
      const rankLabel = isFixed ? '📌 고정' : (isHot ? `🔥 ${rank}위` : `${rank}위`);
      const showRank = mode !== 'random';
      return `
        <div class="ball-wrap">
          <div class="ball ${ballColor(n)} ${isFixed ? 'fixed-ball' : ''}"
               title="${n}번 · 역대 ${FREQ[n]}회 (${rank}위)${isFixed ? ' · 고정번호' : ''}">${n}</div>
          <span class="ball-rank ${isFixed ? 'hot' : isHot ? 'hot' : ''}">${showRank ? rankLabel : ''}</span>
        </div>`;
    }).join('');

    row.innerHTML = `<span class="game-label">#${g + 1}</span><div class="balls">${ballsHTML}</div>`;
    board.appendChild(row);

    /* 볼 순차 등장 */
    row.querySelectorAll('.ball').forEach((ball, i) => {
      setTimeout(() => ball.classList.add('show'), g * 90 + i * 65);
    });

    /* 순위 뱃지 등장 */
    if (mode !== 'random') {
      row.querySelectorAll('.ball-rank').forEach((el, i) => {
        setTimeout(() => el.classList.add('visible'), g * 90 + i * 65 + 350);
      });
    }
  }

  updateStatsHighlight();
}

/* ── 초기화 ── */
function clearBoard() {
  lastPicked = [];
  const board = document.getElementById('board');
  board.innerHTML = '';
  for (let g = 0; g < GAMES; g++) {
    const row = document.createElement('div');
    row.className = 'game-row';
    row.innerHTML = `
      <span class="game-label">#${g + 1}</span>
      <div class="balls">${Array(6).fill('<div class="ball-placeholder"></div>').join('')}</div>`;
    board.appendChild(row);
  }
  updateStatsHighlight();
}

/* ── 통계 패널 ── */
function toggleStats() {
  statsOpen = !statsOpen;
  document.getElementById('statsBody').classList.toggle('open', statsOpen);
  document.getElementById('statsIcon').classList.toggle('open', statsOpen);
}

function sortStats(by) {
  statSort = by;
  document.querySelectorAll('.sort-tab').forEach((el, i) => {
    el.classList.toggle('active', ['freq','asc','rare'][i] === by);
  });
  renderStats();
}

function renderStats() {
  const order = statSort === 'asc'  ? Object.keys(FREQ).map(Number)
              : statSort === 'rare' ? [...BY_FREQ].reverse()
              :                       BY_FREQ;

  const picked = new Set(lastPicked);
  document.getElementById('statsGrid').innerHTML = order.map(n => `
    <div class="stat-card ${picked.has(n) ? 'picked' : ''}" id="sc-${n}">
      <div class="stat-num">${n}</div>
      <div class="stat-bar-wrap">
        <div class="stat-bar" style="width:${(FREQ[n] / MAX_FREQ * 100).toFixed(1)}%"></div>
      </div>
      <div class="stat-count">${FREQ[n]}회</div>
    </div>`).join('');
}

function updateStatsHighlight() {
  const picked = new Set(lastPicked);
  document.querySelectorAll('.stat-card').forEach(el => {
    const n = parseInt(el.id.replace('sc-', ''));
    el.classList.toggle('picked', picked.has(n));
  });
}

/* ── 테마 토글 ── */
function initTheme() {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    document.body.classList.add('dark-mode');
    document.getElementById('themeIcon').textContent = '☀️';
  } else {
    document.body.classList.remove('dark-mode');
    document.getElementById('themeIcon').textContent = '🌙';
  }
}

function toggleTheme() {
  const isDark = document.body.classList.toggle('dark-mode');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  document.getElementById('themeIcon').textContent = isDark ? '☀️' : '🌙';
}

/* ── 초기 렌더 ── */
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    clearBoard();
    renderStats();
});
