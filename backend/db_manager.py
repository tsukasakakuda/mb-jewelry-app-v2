"""
データベース管理モジュール
SQLite/PostgreSQL両対応のデータベース接続管理
"""

import os
import json
from typing import Optional, Dict, List, Union
from datetime import datetime

# 環境変数でデータベースタイプを判定
DB_TYPE = os.getenv('DB_TYPE', 'sqlite')  # 'sqlite' or 'postgresql'

if DB_TYPE == 'postgresql':
    import psycopg2
    import psycopg2.extras
else:
    import sqlite3

class DatabaseManager:
    """データベース管理クラス（SQLite/PostgreSQL両対応）"""
    
    def __init__(self):
        self.db_type = DB_TYPE
        
        if self.db_type == 'postgresql':
            # Cloud SQL PostgreSQL設定
            self.db_config = {
                'host': os.getenv('DB_HOST', '/cloudsql/mb-jewelry-app:asia-northeast1:mb-jewelry-dev'),
                'database': os.getenv('DB_NAME', 'jewelry_db'),
                'user': os.getenv('DB_USER', 'jewelry_user'),
                'password': os.getenv('DB_PASSWORD', ''),
                'port': os.getenv('DB_PORT', '5432'),
            }
        else:
            # SQLite設定（ローカル開発用）
            self.db_path = os.path.join(os.path.dirname(__file__), 'users.db')
    
    def get_connection(self):
        """データベース接続を取得"""
        if self.db_type == 'postgresql':
            conn = psycopg2.connect(**self.db_config)
            return conn
        else:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict]]:
        """クエリを実行して結果を返す"""
        conn = self.get_connection()
        
        try:
            if self.db_type == 'postgresql':
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            else:
                cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                if self.db_type == 'postgresql':
                    return [dict(row) for row in results]
                else:
                    return [dict(row) for row in results]
            else:
                conn.commit()
                return cursor.rowcount
                
        except Exception as e:
            print(f"Database query error: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def execute_insert(self, query: str, params: tuple = None) -> Optional[int]:
        """INSERT文を実行してIDを返す"""
        conn = self.get_connection()
        
        try:
            if self.db_type == 'postgresql':
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # PostgreSQLの場合、RETURNINGを使うかlastrowidの代替
                if 'RETURNING' in query.upper():
                    result = cursor.fetchone()
                    conn.commit()
                    return result[0] if result else None
                else:
                    conn.commit()
                    return cursor.rowcount
            else:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
                return cursor.lastrowid
                
        except Exception as e:
            print(f"Database insert error: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def get_sql_placeholder(self) -> str:
        """SQLプレースホルダーを取得"""
        if self.db_type == 'postgresql':
            return '%s'
        else:
            return '?'
    
    def get_auto_increment_syntax(self) -> str:
        """自動増分カラムの構文を取得"""
        if self.db_type == 'postgresql':
            return 'SERIAL PRIMARY KEY'
        else:
            return 'INTEGER PRIMARY KEY AUTOINCREMENT'
    
    def initialize_tables(self):
        """テーブルを初期化"""
        auto_increment = self.get_auto_increment_syntax()
        
        # ユーザーテーブル
        users_table = f"""
        CREATE TABLE IF NOT EXISTS users (
            id {auto_increment},
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # 計算履歴テーブル
        calculation_history_table = f"""
        CREATE TABLE IF NOT EXISTS calculation_history (
            id {auto_increment},
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
        self.execute_query(users_table)
        self.execute_query(calculation_history_table)
        
        # PostgreSQLの場合、インデックスを作成
        if self.db_type == 'postgresql':
            index_queries = [
                "CREATE INDEX IF NOT EXISTS idx_calculation_history_user_id ON calculation_history (user_id)",
                "CREATE INDEX IF NOT EXISTS idx_calculation_history_created_at ON calculation_history (created_at)",
                "CREATE INDEX IF NOT EXISTS idx_users_username ON users (username)"
            ]
            for query in index_queries:
                try:
                    self.execute_query(query)
                except Exception as e:
                    print(f"Index creation warning: {e}")

# グローバルインスタンス
db_manager = DatabaseManager()