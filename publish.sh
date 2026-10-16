#!/usr/bin/env bash
# ============================================================
# carspecfix — 一键部署到 carspecfix.com
# 路线：干净构建(Astro @ site/) → rsync dist 到 VPS nginx → 确保 vhost → reload → 验证
# 域名走 Cloudflare（橙云，Flexible：CF 终结 TLS，回源 80 端口）
# VPS：data@47.236.224.232（与 pic2emoji / footballclubmenu 同机，互不干扰）
#
# 前置条件：
#   1. Cloudflare zone 已建，DNS A 记录（含 www）指向 47.236.224.232 且橙云开启（Flexible）。
#      —— 需队长本人登录 CF 控制台配置（Agent 无法代登）。
#   2. 本机 ssh 私钥可免密登录 data@47.236.224.232（与兄弟站同机同账号）。
#
# 用法：
#   ./publish.sh            # 完整：构建 + 上传 + vhost + reload + 验证
#   ./publish.sh --dry-run  # 仅本地统计待同步文件，不传输
#
# 注意：请在队长本机真实终端运行。WorkBuddy 沙箱内 ssh 直连 VPS 被出口策略拦截，
#       无法从此处直推；脚本本身是为本机一键部署而写。
# ============================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SITE_DIR="$REPO_ROOT/site"
DIST_DIR="$SITE_DIR/dist"

REMOTE="data@47.236.224.232"
REMOTE_DIR="/data/Htdocs/carspecfix"
VHOST_NAME="carspecfix"
DOMAIN="carspecfix.com"

# ---- 参数解析 ----
DRY_RUN=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    *)
      echo "未知参数: $arg" >&2
      echo "用法: $0 [--dry-run]" >&2
      exit 2
      ;;
  esac
done

echo "==> [1/5] 干净构建 (Astro @ site/)"
cd "$SITE_DIR"
rm -rf dist .astro
npm run build
[ -f "$DIST_DIR/index.html" ] || { echo "构建失败：dist/index.html 未生成" >&2; exit 1; }
echo "    构建完成：$(find "$DIST_DIR" -name '*.html' | wc -l | tr -d ' ') 个 HTML"

echo "==> [2/5] rsync dist -> $REMOTE:$REMOTE_DIR"
if [[ "$DRY_RUN" == "1" ]]; then
  echo "    (dry-run) 待同步文件统计："
  find "$DIST_DIR" -type f | wc -l | tr -d ' ' | sed 's/^/    文件数: /'
  du -sh "$DIST_DIR" | sed 's/^/    体积:   /'
  echo "    (dry-run) 未传输。直接 ./publish.sh 执行真实同步。"
  exit 0
fi
rsync -az --delete --human-readable --exclude '.DS_Store' \
  "$DIST_DIR/" "$REMOTE:$REMOTE_DIR/"

echo "==> [3/5] 确保 nginx vhost 存在（幂等）"
VHOST=$(cat <<'VHOST_EOF'
# carspecfix.com — static export (Astro)
server {
    listen 80;
    listen [::]:80;

    server_name carspecfix.com www.carspecfix.com;

    root /data/Htdocs/carspecfix;
    index index.html;

    charset utf-8;
    server_tokens off;

    access_log /var/log/nginx/carspecfix.access.log;
    error_log /var/log/nginx/carspecfix.error.log warn;

    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_comp_level 5;
    gzip_types
        text/plain
        text/css
        text/xml
        application/json
        application/javascript
        application/xml
        application/rss+xml
        image/svg+xml;

    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    error_page 404 /404.html;
    location = /404.html {
        internal;
    }

    location / {
        try_files $uri $uri/ =404;
    }

    location ~* \.html?$ {
        expires -1;
        add_header Cache-Control "no-cache";
        try_files $uri =404;
    }

    location ~* \.(css|js|mjs|jpg|jpeg|gif|png|svg|webp|avif|ico|woff|woff2|ttf|eot|pdf)$ {
        expires 7d;
        add_header Cache-Control "public";
        access_log off;
        log_not_found off;
        try_files $uri =404;
    }

    location ~ /\.(?!well-known/) {
        deny all;
    }
}
VHOST_EOF
)
B64=$(printf '%s' "$VHOST" | base64 | tr -d '\n')
ssh -o BatchMode=yes "$REMOTE" \
  "echo '$B64' | base64 -d | sudo tee /etc/nginx/sites-available/$VHOST_NAME >/dev/null && sudo ln -sf /etc/nginx/sites-available/$VHOST_NAME /etc/nginx/sites-enabled/$VHOST_NAME && echo '    vhost ok'"

echo "==> [4/5] nginx -t && reload"
ssh -o BatchMode=yes "$REMOTE" "sudo nginx -t 2>&1 && sudo nginx -s reload 2>&1 || true"

echo "==> [5/5] 验证线上"
sleep 1
code=$(curl -s -m 20 -o /tmp/carspecfix-deploy-check.html -w '%{http_code}' "https://$DOMAIN/")
title=$(grep -o '<title>[^<]*</title>' /tmp/carspecfix-deploy-check.html | head -1 | sed 's/<[^>]*>//g')
if [ "$code" = "200" ]; then
  echo "    ✅ 部署成功：https://$DOMAIN/ (HTTP $code)"
  echo "    $title"
else
  echo "    ❌ 验证失败：HTTP $code / $title" >&2
  echo "    排查：CF 缓存可能未刷新（等 1 分钟重试）；源站直查：ssh $REMOTE 'curl -H \"Host: $DOMAIN\" http://127.0.0.1/'" >&2
  exit 1
fi
