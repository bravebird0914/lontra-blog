#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lontra - Markdown記事をHTMLに変換し、記事一覧（JSON）を生成するスクリプト

使い方:
    python scripts/build_blog.py
    
または:
    python3 scripts/build_blog.py
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

# パス設定
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
POSTS_DIR = PROJECT_ROOT / "posts"
POSTS_JSON = PROJECT_ROOT / "posts.json"
TEMPLATE_FILE = PROJECT_ROOT / "_template.html"


def parse_frontmatter(content):
    """
    Markdownのfrontmatterをパースする
    
    Args:
        content: Markdownファイルの内容
        
    Returns:
        (metadata, body): メタデータと本文のタプル
    """
    # frontmatter（--- で囲まれた部分）を抽出
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        return {}, content
    
    frontmatter_text = match.group(1)
    body = match.group(2)
    
    # frontmatterをパース
    metadata = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()
    
    return metadata, body


def markdown_to_html(markdown_text):
    """
    簡易的なMarkdown→HTML変換
    
    より高度な変換が必要な場合は、markdown2やmistune等のライブラリを使用してください
    """
    html = markdown_text
    
    # 行末のバックスラッシュ（\）を改行（<br>）に変換
    # ただし、コードブロック内や既に処理済みの部分は除外
    html = re.sub(r'\\\s*\n', '<br>\n', html)
    
    # 画像リンク: ![alt text](path)
    def replace_image(match):
        alt_text = match.group(1)
        image_path = match.group(2)
        # 相対パス ../images/ を images/ に変換
        image_path = image_path.replace('../images/', 'images/')
        return f'<img src="{image_path}" alt="{alt_text}" />'
    
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, html)
    
    # リンク: [text](url)
    def replace_link(match):
        link_text = match.group(1)
        link_url = match.group(2)
        return f'<a href="{link_url}">{link_text}</a>'
    
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, html)
    
    # 見出し（h1からh3まで）
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # コードブロック
    def replace_code_block(match):
        lang = match.group(1) or ''
        code = match.group(2)
        # HTMLエスケープ
        code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return f'<pre><code class="language-{lang}">{code}</code></pre>'
    
    html = re.sub(r'```(\w*)\n(.*?)```', replace_code_block, html, flags=re.DOTALL)
    
    # インラインコード
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # 太字
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # リスト
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # リストをulタグで囲む
    lines = html.split('\n')
    result = []
    in_list = False
    
    for line in lines:
        if line.strip().startswith('<li>'):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(line)
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(line)
    
    if in_list:
        result.append('</ul>')
    
    html = '\n'.join(result)
    
    # 引用
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # 段落処理（画像や見出しを含む行は段落にしない）
    lines = html.split('\n')
    paragraphs = []
    current_paragraph = []
    
    for line in lines:
        line_stripped = line.strip()
        # 既にHTMLタグで囲まれている要素（見出し、リスト、コードブロック、画像、引用）はそのまま
        if (line_stripped.startswith('<h') or 
            line_stripped.startswith('<ul>') or 
            line_stripped.startswith('</ul>') or 
            line_stripped.startswith('<li>') or 
            line_stripped.startswith('<pre>') or 
            line_stripped.startswith('</pre>') or 
            line_stripped.startswith('<blockquote>') or 
            line_stripped.startswith('</blockquote>') or
            line_stripped.startswith('<img')):
            # 現在の段落を閉じる
            if current_paragraph:
                paragraphs.append('<p>' + ' '.join(current_paragraph) + '</p>')
                current_paragraph = []
            paragraphs.append(line)
        elif line_stripped == '':
            # 空行で段落を区切る
            if current_paragraph:
                paragraphs.append('<p>' + ' '.join(current_paragraph) + '</p>')
                current_paragraph = []
        else:
            # 段落の内容を追加
            current_paragraph.append(line_stripped)
    
    # 残りの段落を閉じる
    if current_paragraph:
        paragraphs.append('<p>' + ' '.join(current_paragraph) + '</p>')
    
    html = '\n'.join(paragraphs)
    
    return html


def load_template():
    """テンプレートHTMLを読み込む"""
    if not TEMPLATE_FILE.exists():
        print(f"⚠️  テンプレートファイル {TEMPLATE_FILE} が見つかりません")
        return None
    
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return f.read()


def generate_html(metadata, body_html, template):
    """記事HTMLを生成"""
    html = template
    
    # タイトル
    html = html.replace('<title>記事タイトル | lontra</title>', 
                       f'<title>{metadata.get("title", "記事")} | lontra</title>')
    html = html.replace('content="記事の説明文をここに記入してください。"',
                       f'content="{metadata.get("excerpt", "")}"')
    
    # 記事ヘッダー
    html = html.replace('<span class="blog-article-date">2024.12.XX</span>',
                       f'<span class="blog-article-date">{metadata.get("date", "").replace("-", ".")}</span>')
    html = html.replace('<span class="blog-article-category">カテゴリー名</span>',
                       f'<span class="blog-article-category">{metadata.get("category", "")}</span>')
    html = html.replace('<h1 class="blog-article-title">記事タイトルをここに入力</h1>',
                       f'<h1 class="blog-article-title">{metadata.get("title", "")}</h1>')
    html = html.replace('<p class="blog-article-excerpt">\n          記事の導入文や要約をここに書きます。読者の興味を引く内容で始めましょう。\n        </p>',
                       f'<p class="blog-article-excerpt">{metadata.get("excerpt", "")}</p>')
    
    # 本文（テンプレートの本文部分を置き換え）
    content_pattern = r'<div class="blog-article-content">.*?</div>'
    replacement = f'<div class="blog-article-content">\n{body_html}\n      </div>'
    html = re.sub(content_pattern, replacement, html, flags=re.DOTALL)
    
    return html


def build_posts():
    """全ての記事をビルドしてJSONを生成"""
    posts = []
    
    # postsディレクトリの確認
    if not POSTS_DIR.exists():
        print(f"⚠️  {POSTS_DIR} が存在しません")
        POSTS_DIR.mkdir(parents=True, exist_ok=True)
        print(f"✅ {POSTS_DIR} を作成しました")
        return
    
    # テンプレート読み込み
    template = load_template()
    if not template:
        return
    
    # .mdファイルを処理
    md_files = sorted(POSTS_DIR.glob("*.md"), reverse=True)
    
    if not md_files:
        print(f"⚠️  {POSTS_DIR} に.mdファイルがありません")
        print(f"📝 サンプル記事を作成するには、posts/ ディレクトリに Markdown ファイルを配置してください")
        # 空のposts.jsonを作成
        with open(POSTS_JSON, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return
    
    for md_file in md_files:
        print(f"📝 処理中: {md_file.name}")
        
        # Markdownを読み込み
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # frontmatterとbodyを分離
        metadata, body = parse_frontmatter(content)
        
        # 必須フィールドのチェック
        required_fields = ['title', 'date', 'category', 'excerpt']
        missing_fields = [field for field in required_fields if field not in metadata]
        
        if missing_fields:
            print(f"⚠️  {md_file.name} に必須フィールドがありません: {', '.join(missing_fields)}")
            continue
        
        # MarkdownをHTMLに変換
        body_html = markdown_to_html(body)
        
        # HTMLファイル名を生成（.md → .html）
        html_filename = md_file.stem + '.html'
        html_path = PROJECT_ROOT / html_filename
        
        # HTMLを生成
        html_content = generate_html(metadata, body_html, template)
        
        # HTMLファイルを保存
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 生成: {html_filename}")
        
        # 記事情報をリストに追加
        post_info = {
            "id": md_file.stem,
            "title": metadata.get("title", ""),
            "date": metadata.get("date", ""),
            "category": metadata.get("category", ""),
            "excerpt": metadata.get("excerpt", ""),
            "file": html_filename
        }
        posts.append(post_info)
    
    # posts.jsonを保存
    with open(POSTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    
    print(f"\n✨ 完了！ {len(posts)}件の記事を処理しました")
    print(f"📄 {POSTS_JSON} を更新しました")


if __name__ == "__main__":
    print("🚀 lontra ビルドを開始します...\n")
    build_posts()
    print("\n✅ ブログビルド完了！")

