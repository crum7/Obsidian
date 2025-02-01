#!/usr/bin/env python3
import os
import re
import urllib.parse

# ここはご自身のリポジトリに合わせて修正
GITHUB_USER = "crum7"
REPO_NAME   = "Obsidian"
BRANCH_NAME = "main"

# .md ファイルの検索を開始するルートディレクトリ（例: カレントディレクトリ）
ROOT_DIR = "."

# Obsidian形式  : ![[filename.png]]
# Markdown形式 : ![](images/filename.png) など
# 壊れたリンク : ![](https://github.com/crum7/Obsidian/blob/main/https://github.com/...)
#   → 主に 2 重 https://github.com/... の場合を想定して置き換え

# 正規表現パターン
# 1) Obsidian形式
PATTERN_OBSIDIAN = re.compile(r'!\[\[(.*?)\]\]')
# 2) Markdown形式でローカルパス
PATTERN_MD_LOCAL = re.compile(r'!\[\]\((images/.*?)\)')
# 3) 壊れリンク(例)
PATTERN_BROKEN   = re.compile(
    r'!\[\]\(https://github\.com/' + re.escape(GITHUB_USER) + '/' + re.escape(REPO_NAME) +
    r'/blob/' + re.escape(BRANCH_NAME) + r'/https://github\.com/' # 2重の GitHub URL
)

def find_image_path(md_file_path: str, image_name: str) -> str:
    """
    Markdownファイルと同じディレクトリ下の images/ を探し、実際のパスを返す。
    例: 
      md_file_path = 'HackTheBox_Writeups/Retired/Easy/some_writeup.md'
      image_name   = 'Pasted image 20250103113531.png'
      → 'HackTheBox_Writeups/Retired/Easy/images/Pasted image 20250103113531.png'
    """
    # Markdownファイルがあるディレクトリを取得
    md_dir = os.path.dirname(md_file_path)

    # Obsidianの記法は拡張子付きのケースが多い想定なので、そのまま使う
    # 必要に応じて .png, .jpg, .jpeg, .gif など補完ロジックをいれるなら追加
    candidate_path = os.path.join(md_dir, "images", image_name)
    return candidate_path

def generate_github_raw_url(local_path: str) -> str:
    """
    ローカルパスを元に、raw.githubusercontent.com のフルURLを生成する。
      例) local_path = 'HackTheBox_Writeups/Retired/Easy/images/Pasted image.png'
         → 'https://raw.githubusercontent.com/<USER>/<REPO>/main/HackTheBox_Writeups/Retired/Easy/images/Pasted%20image.png'
    """
    # パスの区切り文字を統一
    norm_path = os.path.normpath(local_path)

    # URL 用にエンコード (スペースなどを %20 に変換)
    encoded_path = urllib.parse.quote(norm_path)

    # GitHub RAW URL のフォーマット
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH_NAME}/{encoded_path}"

def process_file(md_file_path: str):
    """
    指定された Markdown ファイルを読み込んで、
    画像リンクを正しい raw.githubusercontent.com のリンクへ置き換える。
    """
    with open(md_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    updated = False

    for line in lines:
        original_line = line

        # --- (1) Obsidian形式の置き換え) ![[filename.png]]
        matches = PATTERN_OBSIDIAN.findall(line)
        for m in matches:
            image_name = m.strip()
            # 画像の相対パスを導出
            local_path = find_image_path(md_file_path, image_name)
            # 正しい raw.githubusercontent.com のリンクを生成
            raw_url = generate_github_raw_url(local_path)
            # 置き換え
            line = line.replace(f'![[{image_name}]]', f'![]({raw_url})')

        # --- (2) Markdown形式 (ローカルパスのケース) ![](images/filename.png)
        matches_md_local = PATTERN_MD_LOCAL.findall(line)
        for local_md_path in matches_md_local:
            # local_md_path = 'images/filename.png'
            # 絶対パスに変換
            local_path = os.path.join(os.path.dirname(md_file_path), local_md_path)
            raw_url = generate_github_raw_url(local_path)
            # 置き換え
            line = line.replace(f'({local_md_path})', f'({raw_url})')

        # --- (3) 壊れリンクの修正 (例: 2重の https://github.com/...)
        #         「想定パターン」にマッチしたら、とりあえず抜き取る方式で修正する例
        if PATTERN_BROKEN.search(line):
            # 2重になっている URL を取り除く or 別正規表現で再マッチして適宜修正
            # ここではシンプルに "https://github.com/<USER>/<REPO>/blob/main/" 以降の
            # 2重部分を取り除いて raw URL に書き換える簡易実装とする
            # 実際には各リンクを正規表現で抜き出してrawに変換が必要
            # (細かいケースごとにロジックを追加要)
            line = re.sub(
                r'!\[\]\(https://github\.com/' + re.escape(GITHUB_USER) + '/' + re.escape(REPO_NAME) +
                r'/blob/' + re.escape(BRANCH_NAME) + r'/https://github\.com/.*?\)', 
                # 例として強制的に "[BrokenLink]" に置き換え。
                # 必要に応じて再度ローカルに引き直して raw にするロジックを追加する。
                '![]([BrokenLink])', 
                line
            )

        if line != original_line:
            updated = True

        new_lines.append(line)

    if updated:
        # ファイルを上書き保存
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"[UPDATED] {md_file_path}")
    else:
        print(f"[NO CHANGE] {md_file_path}")


def main():
    # 再帰的に .md ファイルを探し出して処理
    for root, dirs, files in os.walk(ROOT_DIR):
        # .git フォルダなどはスキップしたい場合
        if '.git' in dirs:
            dirs.remove('.git')

        for file in files:
            if file.lower().endswith(".md"):
                md_file_path = os.path.join(root, file)
                process_file(md_file_path)

if __name__ == "__main__":
    main()
