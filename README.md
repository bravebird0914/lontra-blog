# lontra

友人と2人で運営するグルメブログです。

- サイト: https://bravebird0914.github.io/lontra-blog/
- ポートフォリオ: https://bravebird0914.github.io/

## 構成

```
index.html            記事一覧
articles/             公開用 HTML
posts/                原稿（Markdown）
posts.json            一覧データ（自動生成）
css/  js/  images/
scripts/build_blog.py
```

## 記事を追加する

`posts/YYYY-MM-DD-タイトル.md` を作り、先頭にメタデータを書きます。

```markdown
---
title: 記事のタイトル
date: 2024-11-19
category: Restaurant
excerpt: 一覧に出る要約
---

本文
```

ビルドすると `articles/` に HTML が作られ、一覧も更新されます。

```bash
python3 scripts/build_blog.py
git add .
git commit -m "blog: 記事を追加"
git push
```

GitHub Pages の公開ブランチから配信されます。
