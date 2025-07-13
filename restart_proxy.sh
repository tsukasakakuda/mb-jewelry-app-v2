#!/bin/bash

echo "🔧 Cloud SQL Proxy 完全再起動"

# 既存のプロセスを停止
echo "⏹️  既存プロセスを停止中..."
pkill -f cloud-sql-proxy 2>/dev/null || true
sleep 2

# プロジェクトが正しく設定されているか確認
PROJECT_ID=$(gcloud config get-value project)
echo "📋 現在のプロジェクト: $PROJECT_ID"

if [ "$PROJECT_ID" != "mb-jewelry-dev" ]; then
    echo "⚠️  プロジェクトを mb-jewelry-dev に設定中..."
    gcloud config set project mb-jewelry-dev
fi

# 認証情報を再設定
echo "🔐 認証情報を確認中..."
gcloud auth application-default login --quiet 2>/dev/null || echo "認証スキップ"

# Cloud SQL Admin APIが有効か確認
echo "🔌 Cloud SQL Admin APIを有効化中..."
gcloud services enable sqladmin.googleapis.com --project=mb-jewelry-dev

# ポートが使用中でないか確認
if lsof -i :5432 >/dev/null 2>&1; then
    echo "⚠️  ポート5432が使用中です。別のポートを使用します..."
    PORT=5433
else
    PORT=5432
fi

echo "🚀 Cloud SQL Proxyを起動中... (ポート: $PORT)"
echo "接続先: mb-jewelry-dev:asia-northeast1:mb-jewelry-dev"

# Cloud SQL Proxyを起動
cloud-sql-proxy mb-jewelry-dev:asia-northeast1:mb-jewelry-dev \
  --port $PORT \
  --structured-logs &

PROXY_PID=$!
echo "✅ Cloud SQL Proxy起動完了 (PID: $PROXY_PID)"
echo ""
echo "📝 Sequel Ace接続情報:"
echo "  Host: 127.0.0.1"
echo "  Port: $PORT"
echo "  Database: jewelry_db"
echo "  Username: jewelry_user"
echo "  Password: zwa/J5f+vbiKykZTYHk/s9kNyA2bLpu5gmA8wWm+uR4="
echo ""
echo "⏹️  停止するには Ctrl+C を押してください"

# プロセスの監視
wait $PROXY_PID