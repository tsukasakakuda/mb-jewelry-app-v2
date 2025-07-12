#!/bin/bash

# Cloud SQL セットアップスクリプト

echo "🔧 Setting up Cloud SQL for mb-jewelry-app..."

# プロジェクト設定
PROJECT_ID=$(gcloud config get-value project)
INSTANCE_NAME="mb-jewelry-dev"
DATABASE_NAME="jewelry_db"
USER_NAME="jewelry_user"

echo "📋 Project: $PROJECT_ID"
echo "📋 Instance: $INSTANCE_NAME"
echo "📋 Database: $DATABASE_NAME"
echo "📋 User: $USER_NAME"

# インスタンスが作成完了するまで待機
echo "⏳ Waiting for instance to be ready..."
while true; do
    STATUS=$(gcloud sql instances describe $INSTANCE_NAME --format="value(state)" 2>/dev/null)
    if [ "$STATUS" = "RUNNABLE" ]; then
        echo "✅ Instance is ready!"
        break
    elif [ "$STATUS" = "PENDING_CREATE" ]; then
        echo "⏳ Still creating instance... waiting 30 seconds"
        sleep 30
    else
        echo "❌ Unexpected status: $STATUS"
        exit 1
    fi
done

# データベース作成
echo "🗄️ Creating database..."
gcloud sql databases create $DATABASE_NAME --instance=$INSTANCE_NAME

# ユーザー作成とパスワード設定
echo "👤 Creating database user..."
DB_PASSWORD=$(openssl rand -base64 32)
gcloud sql users create $USER_NAME --instance=$INSTANCE_NAME --password="$DB_PASSWORD"

# 権限設定
echo "🔐 Setting up permissions..."
gcloud sql users set-password $USER_NAME --instance=$INSTANCE_NAME --password="$DB_PASSWORD"

# 接続情報を表示
echo ""
echo "✅ Cloud SQL setup completed!"
echo ""
echo "📝 Connection Information:"
echo "   Instance: $INSTANCE_NAME"
echo "   Database: $DATABASE_NAME"
echo "   User: $USER_NAME"
echo "   Password: $DB_PASSWORD"
echo ""
echo "🔗 Connection string for Cloud Run:"
echo "   DB_HOST=/cloudsql/$PROJECT_ID:asia-northeast1:$INSTANCE_NAME"
echo "   DB_NAME=$DATABASE_NAME"
echo "   DB_USER=$USER_NAME"
echo "   DB_PASSWORD=$DB_PASSWORD"
echo ""

# 環境変数ファイル作成
ENV_FILE="cloudsql_env.txt"
cat > $ENV_FILE << EOF
DB_TYPE=postgresql
DB_HOST=/cloudsql/$PROJECT_ID:asia-northeast1:$INSTANCE_NAME
DB_NAME=$DATABASE_NAME
DB_USER=$USER_NAME
DB_PASSWORD=$DB_PASSWORD
DB_PORT=5432
EOF

echo "💾 Environment variables saved to: $ENV_FILE"
echo ""
echo "🚀 Next steps:"
echo "   1. Update Cloud Run service with these environment variables"
echo "   2. Enable Cloud SQL connection in Cloud Run"
echo "   3. Deploy the updated application"