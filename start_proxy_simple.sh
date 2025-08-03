#!/bin/bash

echo "🔧 Cloud SQL Proxy シンプル起動"

# 既存プロセスを停止
pkill -f cloud-sql-proxy 2>/dev/null || true
sleep 2

echo "🚀 Cloud SQL Proxyを起動中..."

# シンプルな起動（デバッグ情報なし）
cloud-sql-proxy mb-jewelry-dev:asia-northeast1:mb-jewelry-dev --port 5432 &

PROXY_PID=$!
echo "✅ Cloud SQL Proxy起動完了 (PID: $PROXY_PID)"
echo ""
echo "📝 Sequel Ace接続情報:"
echo "  Host: 127.0.0.1"
echo "  Port: 5432"
echo "  Database: jewelry_db"
echo "  Username: jewelry_user"
echo "  Password: zwa/J5f+vbiKykZTYHk/s9kNyA2bLpu5gmA8wWm+uR4="
echo ""
echo "⏹️  停止するには Ctrl+C を押してください"

# プロセスの監視
wait $PROXY_PID