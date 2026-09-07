#!/usr/bin/env bash
# 推送后验证。沙箱出网白名单里没有 img2.895832.xyz，curl 不到最终地址，
# 所以改为通过 api.github.com 验证两件事：
#   1. 文件确实在仓库里（Contents API，返回文件大小与 sha）
#   2. 最近一次 Pages 构建成功（Pages builds API，status = built）
# 两条都过，就可以认为公网地址会生效。

set -euo pipefail

: "${GH_USER:?需要 GH_USER}"
: "${GH_REPO:?需要 GH_REPO}"
: "${GH_TOKEN:?需要 GH_TOKEN}"

PREFIX="${PREFIX:-gzh/$(date +%Y/%m)}"
API="https://api.github.com/repos/${GH_USER}/${GH_REPO}"
AUTH=(-H "Authorization: Bearer ${GH_TOKEN}"
      -H "Accept: application/vnd.github+json"
      -H "X-GitHub-Api-Version: 2022-11-28")

fail=0

echo "── 文件检查 ──"
for name in "$@"; do
  name="$(basename "$name")"
  code=$(curl -s -o /tmp/gh_content.json -w '%{http_code}' \
         "${AUTH[@]}" "${API}/contents/${PREFIX}/${name}")
  if [ "$code" = "200" ]; then
    size=$(python3 -c "import json;print(json.load(open('/tmp/gh_content.json'))['size'])")
    echo "  ✓ ${PREFIX}/${name}  (${size} bytes)"
  else
    echo "  ✗ ${PREFIX}/${name}  HTTP ${code}"
    fail=1
  fi
done

echo "── Pages 构建 ──"
code=$(curl -s -o /tmp/gh_pages.json -w '%{http_code}' \
       "${AUTH[@]}" "${API}/pages/builds/latest")
if [ "$code" = "200" ]; then
  python3 - <<'PY'
import json
b = json.load(open('/tmp/gh_pages.json'))
status = b.get('status')
mark = '✓' if status == 'built' else '✗'
print(f"  {mark} status={status}  updated={b.get('updated_at')}")
err = (b.get('error') or {}).get('message')
if err:
    print(f"    error: {err}")
raise SystemExit(0 if status == 'built' else 1)
PY
  [ $? -eq 0 ] || fail=1
else
  echo "  ✗ Pages API HTTP ${code}（Pages 可能还没开）"
  fail=1
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "全部通过。"
else
  echo "有失败项，先别交付。"
fi
exit "$fail"
