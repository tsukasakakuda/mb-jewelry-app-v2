#!/bin/bash

# Cloud SQL Proxy セットアップスクリプト
# Sequel Ace接続用

PROJECT_ID="mb-jewelry-dev"
INSTANCE_NAME="mb-jewelry-dev"
REGION="asia-northeast1"
LOCAL_PORT="5432"

echo "🔧 Cloud SQL Proxy セットアップ"
echo "プロジェクト: $PROJECT_ID"
echo "インスタンス: $INSTANCE_NAME"
echo "ローカルポート: $LOCAL_PORT"
echo ""

# Cloud SQL Proxyがインストールされているかチェック
if ! command -v cloud-sql-proxy &> /dev/null; then
    echo "📥 Cloud SQL Proxyをインストール中..."
    
    # Intel Mac の場合
    if [[ $(uname -m) == "x86_64" ]]; then
        curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.8.0/cloud-sql-proxy.darwin.amd64
    # Apple Silicon Mac の場合
    else
        curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.8.0/cloud-sql-proxy.darwin.arm64
    fi
    
    chmod +x cloud-sql-proxy
    sudo mv cloud-sql-proxy /usr/local/bin/
    echo "✅ Cloud SQL Proxyをインストールしました"
fi

echo "🚀 Cloud SQL Proxyを起動中..."
echo "接続情報:"
echo "  ホスト: localhost"
echo "  ポート: $LOCAL_PORT"
echo "  データベース: jewelry_db"
echo "  ユーザー: jewelry_user"
echo "  パスワード: zwa/J5f+vbiKykZTYHk/s9kNyA2bLpu5gmA8wWm+uR4="
echo ""
echo "📝 Sequel Aceでの接続設定:"
echo "  Name: MB Jewelry Dev"
echo "  Host: localhost"
echo "  Username: jewelry_user"
echo "  Password: zwa/J5f+vbiKykZTYHk/s9kNyA2bLpu5gmA8wWm+uR4="
echo "  Database: jewelry_db"
echo "  Port: $LOCAL_PORT"
echo "  Connection Type: Standard TCP/IP"
echo ""
echo "⚠️  このターミナルウィンドウは開いたままにしてください"
echo "⏹️  停止するには Ctrl+C を押してください"
echo ""

# Cloud SQL Proxyを起動
cloud-sql-proxy $PROJECT_ID:$REGION:$INSTANCE_NAME --port $LOCAL_PORT