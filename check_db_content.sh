#!/bin/bash

# Cloud SQLのテーブル内容確認スクリプト

PROJECT_ID="mb-jewelry-dev"
INSTANCE_NAME="mb-jewelry-dev"
DATABASE_NAME="jewelry_db"
USER_NAME="jewelry_user"

echo "🔍 Cloud SQLテーブル内容確認"
echo "プロジェクト: $PROJECT_ID"
echo "インスタンス: $INSTANCE_NAME"
echo "データベース: $DATABASE_NAME"
echo ""

# SQLクエリをファイルに保存
cat > /tmp/check_tables.sql << 'EOF'
-- テーブル一覧
\dt

-- ユーザーテーブル
SELECT 'users テーブル:' as info;
SELECT id, username, role, created_at FROM users ORDER BY id;

-- 計算履歴テーブル
SELECT 'calculation_history テーブル:' as info;
SELECT id, user_id, calculation_name, total_value, item_count, created_at 
FROM calculation_history ORDER BY created_at DESC LIMIT 10;

-- 統計情報
SELECT 'データベース統計:' as info;
SELECT 
    'users' as table_name, 
    COUNT(*) as record_count 
FROM users
UNION ALL
SELECT 
    'calculation_history' as table_name, 
    COUNT(*) as record_count 
FROM calculation_history;
EOF

echo "📊 テーブル内容を確認中..."

# psqlコマンドでSQLファイルを実行
gcloud sql connect $INSTANCE_NAME --user=$USER_NAME --database=$DATABASE_NAME < /tmp/check_tables.sql 2>/dev/null || {
    echo "❌ 直接接続に失敗しました"
    echo "💡 代替方法: Google Cloud Consoleを使用してください"
    echo "   URL: https://console.cloud.google.com/sql/instances/$INSTANCE_NAME/databases/$DATABASE_NAME?project=$PROJECT_ID"
    echo ""
    echo "📋 または、以下のSQLを手動で実行してください:"
    echo "-- ユーザー一覧"
    echo "SELECT id, username, role, created_at FROM users;"
    echo ""
    echo "-- 計算履歴一覧"
    echo "SELECT id, user_id, calculation_name, total_value, item_count, created_at FROM calculation_history ORDER BY created_at DESC LIMIT 10;"
}

# 一時ファイルを削除
rm -f /tmp/check_tables.sql