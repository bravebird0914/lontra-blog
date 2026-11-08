// ========================================
// lontra - メインJavaScript
// ========================================

// 日付と曜日の表示
function updateCurrentDate() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const weekdays = ['日', '月', '火', '水', '木', '金', '土'];
  const weekday = weekdays[now.getDay()];

  const dateYear = document.querySelector('.date-year');
  const dateMonthDay = document.querySelector('.date-month-day');
  const dateWeekday = document.querySelector('.date-weekday');

  if (dateYear) dateYear.textContent = year;
  if (dateMonthDay) dateMonthDay.textContent = `${month}.${day}`;
  if (dateWeekday) dateWeekday.textContent = weekday;
}

// DOMが完全に読み込まれてから実行
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', updateCurrentDate);
} else {
  updateCurrentDate();
}

// 日付が変わったら更新（午前0時に更新）
setTimeout(() => {
  const now = new Date();
  const tomorrow = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);
  const timeUntilMidnight = tomorrow - now;
  setTimeout(() => {
    updateCurrentDate();
    setInterval(updateCurrentDate, 24 * 60 * 60 * 1000);
  }, timeUntilMidnight);
}, 100);

// スムーススクロール
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    
    if (href === '#' || !href) return;
    
    const target = document.querySelector(href);
    if (!target) return;

    e.preventDefault();
    
    target.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });

    history.pushState(null, '', href);
  });
});

// 外部リンクを新しいタブで開く
document.querySelectorAll('a[href^="http"]').forEach(link => {
  if (!link.hostname.includes(window.location.hostname)) {
    link.setAttribute('target', '_blank');
    link.setAttribute('rel', 'noopener noreferrer');
  }
});

// 右上の日付をすばやく3回押すと、カワウソが一度だけ横切る
function initSecretOtter() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const trigger = document.querySelector('.current-date');
  if (!trigger) return;

  let taps = 0;
  let resetTimer = 0;

  trigger.addEventListener('click', () => {
    taps += 1;
    window.clearTimeout(resetTimer);
    resetTimer = window.setTimeout(() => {
      taps = 0;
    }, 700);
    if (taps < 3) return;
    taps = 0;
    passOtter();
  });
}

function passOtter() {
  let otter = document.querySelector('.secret-otter');
  if (!otter) {
    otter = document.createElement('div');
    otter.className = 'secret-otter';
    otter.setAttribute('aria-hidden', 'true');
    otter.innerHTML = `
      <svg viewBox="0 0 120 64" width="96" height="52" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="34" cy="40" rx="28" ry="14" fill="#6e4430"/>
        <ellipse cx="40" cy="42" rx="16" ry="8" fill="#f4dec6"/>
        <circle cx="62" cy="30" r="14" fill="#6e4430"/>
        <circle cx="56" cy="20" r="4" fill="#6e4430"/>
        <circle cx="68" cy="19" r="4" fill="#6e4430"/>
        <ellipse cx="72" cy="32" rx="7" ry="5" fill="#f4deC6"/>
        <circle cx="77" cy="31" r="2.2" fill="#2a1e1a"/>
        <circle cx="66" cy="28" r="1.7" fill="#2a1e1a"/>
        <ellipse cx="58" cy="44" rx="5" ry="3" fill="#4e3022"/>
        <ellipse cx="78" cy="46" rx="5" ry="3" fill="#4e3022"/>
      </svg>
    `;
    document.body.appendChild(otter);
  }

  otter.classList.remove('is-swimming');
  void otter.offsetWidth;
  otter.classList.add('is-swimming');
  otter.addEventListener('animationend', () => {
    otter.classList.remove('is-swimming');
  }, { once: true });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initSecretOtter);
} else {
  initSecretOtter();
}

