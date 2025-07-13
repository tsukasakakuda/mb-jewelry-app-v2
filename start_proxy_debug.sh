#!/bin/bash

echo "🔧 Cloud SQL Proxy デバッグモードで起動"

# Cloud SQL Proxyを詳細ログ付きで起動
cloud-sql-proxy mb-jewelry-dev:asia-northeast1:mb-jewelry-dev \
  --port 5432 \
  --verbose \
  --structured-logs &

PROXY_PID=$!
echo "🚀 Cloud SQL Proxy起動 (PID: $PROXY_PID)"
echo "📝 接続情報:"
echo "  Host: 127.0.0.1"
echo "  Port: 5432"
echo "  Database: jewelry_db"
echo "  Username: jewelry_user"
echo "  Password: zwa/J5f+vbiKykZTYHk/s9kNyA2bLpu5gmA8wWm+uR4="

# 5秒待機してから接続テスト
sleep 5

echo ""
echo "🧪 接続テスト中..."
if command -v psql >/dev/null 2>&1; then
    PGPASSWORD='zwa/J5f+vbiKykZTYHk/s9kNyA2bLpu5gmA8wWm+uR4=' psql \
      -h 127.0.0.1 \
      -p 5432 \
      -U jewelry_user \
      -d jewelry_db \
      -c "SELECT 'Connection successful!' as status;" 2>/dev/null && echo "✅ 接続テスト成功" || echo "❌ 接続テスト失敗"
else
    echo "⚠️  psqlが見つかりません。手動でSequel Aceをテストしてください"
fi

echo ""
echo "⏹️  停止するには Ctrl+C を押してください"
wait $PROXY_PID