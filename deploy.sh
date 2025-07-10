#!/bin/bash

# デプロイ用シェルスクリプト
# 使用方法: ./deploy.sh [PROJECT_ID] [REGION]

PROJECT_ID=${1:-"your-project-id"}
REGION=${2:-"asia-northeast1"}
SERVICE_NAME="mb-jewelry-app"

echo "🚀 GCPプロジェクト: $PROJECT_ID"
echo "🌏 リージョン: $REGION"
echo "📦 サービス名: $SERVICE_NAME"

# 1. フロントエンドのビルド
echo "📦 フロントエンドをビルド中..."
cd frontend
npm ci
npm run build
cd ..

# 2. gcloudの設定確認
echo "⚙️ gcloudプロジェクトを設定中..."
gcloud config set project $PROJECT_ID

# 3. Cloud Runにデプロイ
echo "☁️ Cloud Runにデプロイ中..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300s

echo "✅ デプロイ完了!"
echo "🔗 URL: https://$SERVICE_NAME-$(gcloud config get-value project | tr '[:upper:]' '[:lower:]')-$REGION.a.run.app"