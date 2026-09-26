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

// デバッグ用
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
  console.log('✨ lontra loaded');
}

