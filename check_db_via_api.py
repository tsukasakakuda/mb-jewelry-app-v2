#!/usr/bin/env python3
"""
Cloud Run経由でデータベース内容を確認するスクリプト
"""

import sys
import os

# バックエンドディレクトリをパスに追加
sys.path.append('/Users/tsukasakakuda/dev/mb-jewelry-app/backend')

# 環境変数設定
os.environ['DB_TYPE'] = 'postgresql'
os.environ['DB_HOST'] = '/cloudsql/mb-jewelry-dev:asia-northeast1:mb-jewelry-dev'
os.environ['DB_NAME'] = 'jewelry_db'
os.environ['DB_USER'] = 'jewelry_user'
os.environ['DB_PASSWORD'] = 'zwa/J5f+vbiKykZTYHk/s9kNyA2bLpu5gmA8wWm+uR4='
os.environ['DB_PORT'] = '5432'

def check_database_content():
    """データベース内容を確認"""
    try:
        from db_manager import db_manager
        
        print("🔍 Cloud SQLデータベース内容確認")
        print("="*50)
        
        # ユーザーテーブル
        print("\n👤 ユーザーテーブル:")
        users = db_manager.execute_query("SELECT id, username, role, created_at FROM users ORDER BY id")
        if users:
            for user in users:
                print(f"  ID: {user['id']}, ユーザー名: {user['username']}, ロール: {user['role']}, 作成日: {user['created_at']}")
        else:
            print("  データがありません")
        
        # 計算履歴テーブル
        print("\n📊 計算履歴テーブル（最新10件）:")
        histories = db_manager.execute_query("""
            SELECT id, user_id, calculation_name, total_value, item_count, created_at 
            FROM calculation_history 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        if histories:
            for history in histories:
                print(f"  ID: {history['id']}, ユーザー: {history['user_id']}, 名前: {history['calculation_name']}")
                print(f"    総額: {history['total_value']}, アイテム数: {history['item_count']}, 作成日: {history['created_at']}")
        else:
            print("  データがありません")
        
        # 統計情報
        print("\n📈 統計情報:")
        user_count = db_manager.execute_query("SELECT COUNT(*) as count FROM users")
        history_count = db_manager.execute_query("SELECT COUNT(*) as count FROM calculation_history")
        
        print(f"  ユーザー数: {user_count[0]['count'] if user_count else 0}")
        print(f"  計算履歴数: {history_count[0]['count'] if history_count else 0}")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("⚠️  注意: このスクリプトはCloud Run環境でのみ動作します")
    print("ローカル環境では psycopg2 がインストールされていないため実行できません")
    print("")
    print("代替手段:")
    print("1. Google Cloud Console: https://console.cloud.google.com/sql/instances/mb-jewelry-dev")
    print("2. Cloud Shell経由での接続")
    print("3. pgAdmin等のクライアントツール")