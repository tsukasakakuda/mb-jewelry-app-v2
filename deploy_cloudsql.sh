#!/bin/bash

# Cloud SQL対応デプロイスクリプト
# 使用方法: ./deploy_cloudsql.sh [PROJECT_ID] [REGION]

PROJECT_ID=${1:-$(gcloud config get-value project)}
REGION=${2:-"asia-northeast1"}
SERVICE_NAME="mb-jewelry-dev"
INSTANCE_NAME="mb-jewelry-dev"

echo "🚀 GCPプロジェクト: $PROJECT_ID"
echo "🌏 リージョン: $REGION"
echo "📦 サービス名: $SERVICE_NAME"
echo "🗄️ Cloud SQLインスタンス: $INSTANCE_NAME"

# 1. フロントエンドのビルド
echo "📦 フロントエンドをビルド中..."
cd frontend
npm ci
npm run build
cd ..

# 2. gcloudの設定確認
echo "⚙️ gcloudプロジェクトを設定中..."
gcloud config set project $PROJECT_ID

# 3. 環境変数ファイルの確認
ENV_FILE="cloudsql_env.txt"
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Cloud SQL環境変数ファイルが見つかりません: $ENV_FILE"
    echo "   setup_cloudsql.sh を実行してCloud SQLを設定してください"
    exit 1
fi

echo "📋 環境変数を読み込み中..."
source $ENV_FILE

# 4. Cloud Runにデプロイ（Cloud SQL接続付き）
echo "☁️ Cloud Runにデプロイ中（Cloud SQL接続付き）..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300s \
  --add-cloudsql-instances "$PROJECT_ID:$REGION:$INSTANCE_NAME" \
  --set-env-vars "DB_TYPE=$DB_TYPE,DB_HOST=$DB_HOST,DB_NAME=$DB_NAME,DB_USER=$DB_USER,DB_PASSWORD=$DB_PASSWORD,DB_PORT=$DB_PORT"

echo "✅ デプロイ完了!"
echo "🔗 URL: https://$SERVICE_NAME-$(echo $PROJECT_ID | tr '[:upper:]' '[:lower:]')-$REGION.a.run.app"
echo ""
echo "📊 Cloud SQL接続情報:"
echo "   インスタンス: $INSTANCE_NAME"
echo "   データベース: $DB_NAME"
echo "   ユーザー: $DB_USER"