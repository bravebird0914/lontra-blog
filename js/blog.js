// ========================================
// lontra - ブログ記事自動読み込み
// ========================================

/**
 * posts.jsonから記事一覧を取得してカード表示
 */
async function loadBlogPosts() {
  try {
    // GitHub Pages サブディレクトリ対応
    const basePath = window.location.pathname.includes('/lontra-blog/') 
      ? '/lontra-blog/' 
      : '/';
    
    // posts.jsonを取得
    const response = await fetch(`${basePath}posts.json`);
    if (!response.ok) {
      console.warn('posts.jsonが見つかりません');
      return;
    }
    
    const posts = await response.json();
    
    // ブログ一覧ページ
    const blogGrid = document.querySelector('#blog-grid');
    if (blogGrid && posts.length > 0) {
      renderBlogCards(posts, blogGrid);
    }
    
  } catch (error) {
    console.error('記事の読み込みに失敗しました:', error);
  }
}

/**
 * ブログカードをレンダリング
 * @param {Array} posts - 記事データの配列
 * @param {HTMLElement} container - 挿入先のコンテナ
 */
function renderBlogCards(posts, container) {
  // 既存の記事カード（準備中以外）をクリア
  const existingCards = container.querySelectorAll('.blog-card:not(.blog-card-coming-soon)');
  existingCards.forEach(card => card.remove());
  
  // 準備中カードを取得（あれば最後に移動）
  const comingSoonCard = container.querySelector('.blog-card-coming-soon');
  
  // 記事を新しい順にソート
  const sortedPosts = [...posts].sort((a, b) => {
    return new Date(b.date) - new Date(a.date);
  });
  
  // 新しいカードを作成
  sortedPosts.forEach(post => {
    const card = createBlogCard(post);
    
    // 準備中カードの前に挿入
    if (comingSoonCard) {
      container.insertBefore(card, comingSoonCard);
    } else {
      container.appendChild(card);
    }
  });
}

/**
 * ブログカード要素を作成
 * @param {Object} post - 記事データ
 * @returns {HTMLElement} カード要素
 */
function createBlogCard(post) {
  const card = document.createElement('div');
  card.className = 'blog-card';
  
  // 日付をフォーマット（YYYY-MM-DD → YYYY.MM.DD）
  const formattedDate = post.date.replace(/-/g, '.');
  
  card.innerHTML = `
    <div class="blog-card-meta">
      <span class="blog-card-date">${formattedDate}</span>
      <span class="blog-card-category">${post.category}</span>
    </div>
    <h3 class="blog-card-title">
      <a href="${post.file}">${escapeHtml(post.title)}</a>
    </h3>
    <p class="blog-card-excerpt">
      ${escapeHtml(post.excerpt)}
    </p>
    <a href="${post.file}" class="blog-card-link">
      <span>Read More</span>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="5" y1="12" x2="19" y2="12"></line>
        <polyline points="12 5 19 12 12 19"></polyline>
      </svg>
    </a>
  `;
  
  return card;
}

/**
 * HTMLエスケープ
 * @param {string} text - エスケープするテキスト
 * @returns {string} エスケープされたテキスト
 */
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// ページ読み込み時に実行
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', loadBlogPosts);
} else {
  loadBlogPosts();
}

