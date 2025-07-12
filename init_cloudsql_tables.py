#!/usr/bin/env python3
"""
Cloud SQLのテーブル初期化スクリプト
"""

import os
import psycopg2
import bcrypt

# 環境変数から接続情報を取得
DB_CONFIG = {
    'host': '/cloudsql/mb-jewelry-dev:asia-northeast1:mb-jewelry-dev',
    'database': 'jewelry_db',
    'user': 'jewelry_user',
    'password': 'zwa/J5f+vbiKykZTYHk/s9kNyA2bLpu5gmA8wWm+uR4=',
    'port': '5432',
}

def create_tables():
    """テーブルを作成"""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # ユーザーテーブル
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # 計算履歴テーブル
        calculation_history_table = """
        CREATE TABLE IF NOT EXISTS calculation_history (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            calculation_name VARCHAR(255) NOT NULL,
            calculation_data TEXT NOT NULL,
            total_value DECIMAL(15, 2),
            item_count INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
        
        # テーブル作成
        cursor.execute(users_table)
        cursor.execute(calculation_history_table)
        
        # インデックス作成
        index_queries = [
            "CREATE INDEX IF NOT EXISTS idx_calculation_history_user_id ON calculation_history (user_id)",
            "CREATE INDEX IF NOT EXISTS idx_calculation_history_created_at ON calculation_history (created_at)",
            "CREATE INDEX IF NOT EXISTS idx_users_username ON users (username)"
        ]
        
        for query in index_queries:
            cursor.execute(query)
        
        # デフォルト管理者ユーザーを作成
        cursor.execute("SELECT id FROM users WHERE username = %s", ('admin',))
        if not cursor.fetchone():
            admin_password = 'admin123'
            password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                ('admin', password_hash.decode('utf-8'), 'admin')
            )
        
        conn.commit()
        print("✅ Cloud SQLテーブルの初期化が完了しました")
        print("📝 デフォルトユーザー: admin / admin123")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_tables()