#!/bin/bash

echo "🗄️ staging環境データベースセットアップ"

export PROJECT_ID="mb-jewelry-staging"
export INSTANCE_NAME="mb-jewelry-staging"
export DB_NAME="jewelry_db"
export DB_USER="jewelry_user"
export DB_PASSWORD="StagingPass2025!"

echo "⏳ Cloud SQLインスタンスの準備完了を待機中..."
gcloud sql instances describe $INSTANCE_NAME --project=$PROJECT_ID --format="value(state)"

echo "🔧 データベースを作成中..."
gcloud sql databases create $DB_NAME --instance=$INSTANCE_NAME --project=$PROJECT_ID

echo "👤 データベースユーザーを作成中..."
gcloud sql users create $DB_USER --instance=$INSTANCE_NAME --password=$DB_PASSWORD --project=$PROJECT_ID

echo "🌐 ネットワークアクセス許可を設定中..."
gcloud sql instances patch $INSTANCE_NAME --authorized-networks=0.0.0.0/0 --project=$PROJECT_ID

echo "✅ staging環境データベースセットアップ完了"
echo ""
echo "📋 接続情報:"
echo "  Host: /cloudsql/${PROJECT_ID}:asia-northeast1:${INSTANCE_NAME}"
echo "  Database: $DB_NAME"
echo "  User: $DB_USER"
echo "  Password: $DB_PASSWORD"