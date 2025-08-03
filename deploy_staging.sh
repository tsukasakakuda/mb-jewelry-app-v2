#!/bin/bash

# staging環境デプロイスクリプト
# Cloud SQL対応版

echo "🚀 staging環境デプロイ開始"
echo "🚀 GCPプロジェクト: mb-jewelry-staging"
echo "🌏 リージョン: asia-northeast1"
echo "📦 サービス名: mb-jewelry-staging"
echo "🗄️ Cloud SQLインスタンス: mb-jewelry-staging"

# 環境変数設定
export PROJECT_ID="mb-jewelry-staging"
export REGION="asia-northeast1"
export SERVICE_NAME="mb-jewelry-staging"
export INSTANCE_NAME="mb-jewelry-staging"

# データベース設定
export DB_TYPE="postgresql"
export DB_HOST="/cloudsql/${PROJECT_ID}:${REGION}:${INSTANCE_NAME}"
export DB_NAME="jewelry_db"
export DB_USER="jewelry_user"
export DB_PASSWORD="StagingPass2025!"
export DB_PORT="5432"

echo "📦 フロントエンドをビルド中..."
cd frontend
npm install
npm run build
cd ..

echo "⚙️ gcloudプロジェクトを設定中..."
gcloud config set project $PROJECT_ID

echo "📋 環境変数を読み込み中..."
echo "DB_TYPE: $DB_TYPE"
echo "DB_HOST: $DB_HOST"
echo "DB_NAME: $DB_NAME"
echo "DB_USER: $DB_USER"
echo "DB_PORT: $DB_PORT"

echo "☁️ Cloud Runにデプロイ中（Cloud SQL接続付き）..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars "DB_TYPE=$DB_TYPE,DB_HOST=$DB_HOST,DB_NAME=$DB_NAME,DB_USER=$DB_USER,DB_PASSWORD=$DB_PASSWORD,DB_PORT=$DB_PORT" \
  --add-cloudsql-instances "$PROJECT_ID:$REGION:$INSTANCE_NAME" \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 300

echo "✅ staging環境デプロイ完了"
echo "🌐 URL: https://mb-jewelry-staging-gg4m6jtieq-an.a.run.app"