#!/bin/bash

# Cloud SQLでテーブル初期化

PROJECT_ID="mb-jewelry-dev"
INSTANCE_NAME="mb-jewelry-dev"
DATABASE_NAME="jewelry_db"

echo "🗄️ Cloud SQLでテーブルを初期化中..."

# SQLファイルを作成
cat > /tmp/init_tables.sql << 'EOF'
-- ユーザーテーブル
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 計算履歴テーブル
CREATE TABLE IF NOT EXISTS calculation_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    calculation_name VARCHAR(255) NOT NULL,
    calculation_data TEXT NOT NULL,
    total_value DECIMAL(15, 2),
    item_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- インデックス作成
CREATE INDEX IF NOT EXISTS idx_calculation_history_user_id ON calculation_history (user_id);
CREATE INDEX IF NOT EXISTS idx_calculation_history_created_at ON calculation_history (created_at);
CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);

-- デフォルト管理者ユーザー（パスワード: admin123のハッシュ）
INSERT INTO users (username, password_hash, role) 
VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LlMwMMBcWKnV9/p5G', 'admin')
ON CONFLICT (username) DO NOTHING;
EOF

# Cloud SQLでSQLを実行
gcloud sql import sql $INSTANCE_NAME gs://temp-sql-import-bucket/init_tables.sql --database=$DATABASE_NAME 2>/dev/null || {
    echo "📋 Cloud SQLで直接テーブルを作成中..."
    # psqlコマンドで直接実行
    gcloud sql connect $INSTANCE_NAME --user=jewelry_user --database=jewelry_db < /tmp/init_tables.sql
}

echo "✅ テーブル初期化完了"
echo "👤 デフォルトユーザー: admin / admin123"