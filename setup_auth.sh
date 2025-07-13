#!/bin/bash

echo "🔐 Cloud SQL用認証セットアップ"

# 環境変数を完全にクリア
unset GOOGLE_APPLICATION_CREDENTIALS
export GOOGLE_APPLICATION_CREDENTIALS=""

echo "📋 現在の認証状況:"
gcloud auth list

echo "🔧 プロジェクトを設定中..."
gcloud config set project mb-jewelry-dev

echo "🔑 Application Default Credentialsを設定中..."
echo "ブラウザが開きます。Googleアカウントでログインしてください。"

# Application Default Credentialsを設定
gcloud auth application-default login --project=mb-jewelry-dev

echo "✅ 認証完了"
echo ""
echo "次のコマンドでプロキシを起動してください:"
echo "./start_proxy_simple.sh"