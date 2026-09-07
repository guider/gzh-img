#!/usr/bin/env bash
# 把待传 PNG 推进 GitHub 图床仓库，并打印公网地址。
#
# 依赖三个环境变量（放在项目知识里，每次会话开头 export 一遍）：
#   GH_USER   GitHub 用户名
#   GH_REPO   图床仓库名，例如 gzh-img
#   GH_TOKEN  细粒度 PAT，权限仅 Contents: Read and write，只勾这一个仓库
#
# 用法：
#   bash publish.sh ~/outputs/r2-upload/*.png
#
# 幂等：文件名是内容 sha1，仓库里已存在同名文件就跳过，不产生空提交。

set -euo pipefail

: "${GH_USER:?需要 GH_USER}"
: "${GH_REPO:?需要 GH_REPO}"
: "${GH_TOKEN:?需要 GH_TOKEN}"

PREFIX="${PREFIX:-gzh/$(date +%Y/%m)}"
WORK="${WORK:-$HOME/.gh-imghost-clone}"
DOMAIN="${DOMAIN:-img2.895832.xyz}"

if [ "$#" -eq 0 ]; then
  echo "用法: bash publish.sh <图片1.png> [图片2.png ...]" >&2
  exit 2
fi

# --- 克隆或更新仓库（--depth 1，图床仓库历史没用） ---
if [ -d "$WORK/.git" ]; then
  git -C "$WORK" remote set-url origin \
    "https://${GH_USER}:${GH_TOKEN}@github.com/${GH_USER}/${GH_REPO}.git"
  git -C "$WORK" fetch --depth 1 -q origin
  git -C "$WORK" reset --hard -q origin/main
else
  rm -rf "$WORK"
  git clone --depth 1 -q \
    "https://${GH_USER}:${GH_TOKEN}@github.com/${GH_USER}/${GH_REPO}.git" "$WORK"
fi

git -C "$WORK" config user.email "claude@localhost"
git -C "$WORK" config user.name  "gzh-typesetter"

mkdir -p "$WORK/$PREFIX"

added=0
urls=()
for src in "$@"; do
  [ -f "$src" ] || { echo "跳过（不存在）: $src" >&2; continue; }
  case "$src" in
    *.png|*.PNG) ;;
    *) echo "跳过（只收 PNG）: $src" >&2; continue ;;
  esac

  name="$(basename "$src")"
  dest="$WORK/$PREFIX/$name"

  if [ -f "$dest" ] && cmp -s "$src" "$dest"; then
    echo "已存在，跳过: $PREFIX/$name"
  else
    cp "$src" "$dest"
    git -C "$WORK" add "$PREFIX/$name"
    added=$((added + 1))
    echo "新增: $PREFIX/$name"
  fi
  urls+=("https://${DOMAIN}/${PREFIX}/${name}")
done

if [ "$added" -gt 0 ]; then
  git -C "$WORK" commit -q -m "add ${added} image(s) [$(date +%F\ %T)]"
  git -C "$WORK" push -q origin main
  echo "已推送 $added 张，等 Pages 构建（约 30–60 秒）"
else
  echo "没有新文件，跳过推送"
fi

echo
echo "公网地址："
for u in "${urls[@]}"; do echo "  $u"; done

# 把 token 从 remote 里擦掉，避免留在磁盘上的 .git/config 里
git -C "$WORK" remote set-url origin \
  "https://github.com/${GH_USER}/${GH_REPO}.git"
