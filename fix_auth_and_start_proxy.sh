#!/bin/bash

echo "🔧 認証修正とCloud SQL Proxy起動"

# 既存プロセスを停止
pkill -f cloud-sql-proxy 2>/dev/null || true

echo "🔐 認証を修正中..."

# 環境変数をクリア
unset GOOGLE_APPLICATION_CREDENTIALS

# プロジェクトを明示的に設定
gcloud config set project mb-jewelry-dev

# Application Default Credentialsを再設定
echo "📋 Application Default Credentialsを設定中..."
gcloud auth application-default login --quiet --project=mb-jewelry-dev 2>/dev/null || {
    echo "⚠️  手動認証が必要です。以下のコマンドを実行してください:"
    echo "gcloud auth application-default login --project=mb-jewelry-dev"
    exit 1
}

# Cloud SQL Admin APIを有効化
echo "🔌 Cloud SQL Admin APIを有効化中..."
gcloud services enable sqladmin.googleapis.com --project=mb-jewelry-dev

echo "⏳ API有効化の反映を待機中... (30秒)"
sleep 30

echo "🚀 Cloud SQL Proxyを起動中..."

# Cloud SQL Proxyを起動
GOOGLE_APPLICATION_CREDENTIALS="" cloud-sql-proxy mb-jewelry-dev:asia-northeast1:mb-jewelry-dev --port 5432 &

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