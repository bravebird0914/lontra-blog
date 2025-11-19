# lontra

友人と2人で運営するグルメブログサイトです。

## 🔗 リンク

- **GitHub Pages**: https://bravebird0914.github.io/lontra-blog/
- **Portfolio Site**: https://bravebird0914.github.io/

## 📖 概要

このブログでは、美味しいお店や料理の記録・感想を共有しています。

## ✨ 特徴

- 🌙 **ダークモード対応**（自動保存、システム設定連動）
- 🎨 **アクアマリン寒色系カラースキーム**（ポートフォリオと統一感のあるデザイン）
- 📱 **完全レスポンシブデザイン**
- ⚡ **高速な静的サイト**
- ✍️ **Markdownで記事を簡単に作成**
- ♿ **アクセシビリティ対応**

## 📁 ディレクトリ構造

```
lontra-blog/
├── index.html          # 記事一覧ページ
├── _template.html      # 記事テンプレート
├── posts.json          # 記事メタデータ（自動生成）
├── css/
│   └── style.css       # スタイルシート
├── js/
│   ├── main.js         # メインJavaScript
│   └── blog.js         # ブログ記事読み込み
├── images/             # 画像ファイル
├── posts/              # Markdown記事ファイル
│   └── *.md
├── scripts/
│   └── build_blog.py   # ビルドスクリプト
└── README.md
```

## 📝 記事の書き方

### 1. Markdownファイルを作成

`posts/` ディレクトリに新しい `.md` ファイルを作成します。

**ファイル名の形式**: `YYYY-MM-DD-記事タイトル.md`

例: `2024-11-19-first-post.md`

### 2. Frontmatterを記述

ファイルの先頭に以下の形式でメタデータを記述します：

```markdown
---
title: 記事のタイトル
date: 2024-11-19
category: Restaurant
excerpt: 記事の要約文。一覧ページに表示されます。
---

# 見出し

本文をMarkdownで書きます。

## 小見出し

- リスト項目1
- リスト項目2

コードブロックも使えます：

\`\`\`python
print("Hello, World!")
\`\`\`
```

### 3. ビルドスクリプトを実行

```bash
cd /Users/bravebird/projects/private/lontra-blog
python3 scripts/build_blog.py
```

これで自動的に：
- ✅ HTMLファイルが生成される
- ✅ `posts.json` が更新される
- ✅ 記事一覧に自動表示される

### 4. GitHubにプッシュ

```bash
git add .
git commit -m "blog: 新しい記事を追加"
git push origin main
```

GitHub Pagesで自動的に公開されます！

## 🎨 デザインのカスタマイズ

### カラースキーム

`css/style.css` の以下のカラーコードを変更できます：

- メインカラー: `#7FFFD4` (Aquamarine)
- アクセントカラー: `#00CED1` (Dark Turquoise)

### サイドバー

`index.html` と `_template.html` のサイドバー部分を編集できます。

## 🤝 共同編集

### Collaboratorの追加方法

1. リポジトリの **Settings** → **Collaborators** → **Add people**
2. 友人のGitHubユーザー名を追加
3. 友人が招待を承認すれば、共同編集が可能になります

### ブランチ戦略（推奨）

```bash
# 新しい記事を書く時
git checkout -b article/記事名
# 編集・コミット
git add .
git commit -m "blog: 記事を追加"
# プッシュしてプルリクエスト
git push origin article/記事名
```

## 🚀 デプロイ

GitHub Pagesの設定：

1. リポジトリの **Settings** → **Pages**
2. **Source**: `main` ブランチを選択
3. 自動的に `https://bravebird0914.github.io/lontra-blog/` で公開されます

## 🛠️ 技術スタック

- **フロントエンド**: HTML/CSS/JavaScript（バニラJS）
- **ビルドツール**: Python 3
- **フォント**: Google Fonts (Playfair Display, Montserrat, Noto Sans JP)
- **ホスティング**: GitHub Pages

## 📄 ライセンス

© 2025 lontra Contributors. All rights reserved.

---

## 🔧 トラブルシューティング

### 記事が表示されない場合

1. `posts.json` が正しく生成されているか確認
2. ビルドスクリプトを再実行
3. ブラウザのキャッシュをクリア

### GitHub Pagesで表示されない場合

1. リポジトリの Settings → Pages で設定を確認
2. `main` ブランチが選択されているか確認
3. 数分待ってから再度アクセス

---

**Happy Blogging! 📝✨**

---

*lontra - 美味しいグルメを記録・共有する場所*

