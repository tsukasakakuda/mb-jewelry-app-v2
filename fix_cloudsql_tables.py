#!/usr/bin/env python3
"""
Cloud SQL接続テストとテーブル初期化
"""

import os
import sys

# 環境変数設定
os.environ['DB_TYPE'] = 'postgresql'
os.environ['DB_HOST'] = '/cloudsql/mb-jewelry-dev:asia-northeast1:mb-jewelry-dev'
os.environ['DB_NAME'] = 'jewelry_db'
os.environ['DB_USER'] = 'jewelry_user'
os.environ['DB_PASSWORD'] = 'zwa/J5f+vbiKykZTYHk/s9kNyA2bLpu5gmA8wWm+uR4='
os.environ['DB_PORT'] = '5432'

try:
    # バックエンドディレクトリをパスに追加
    sys.path.append('/Users/tsukasakakuda/dev/mb-jewelry-app/backend')
    
    from db_manager import db_manager
    from user_manager_v2 import UserManager
    
    print("🔗 Cloud SQL接続テスト中...")
    
    # 接続テスト
    conn = db_manager.get_connection()
    print("✅ Cloud SQL接続成功")
    conn.close()
    
    # テーブル初期化
    print("🗄️ テーブル初期化中...")
    db_manager.initialize_tables()
    print("✅ テーブル作成完了")
    
    # ユーザー管理の初期化
    print("👤 ユーザー管理初期化中...")
    user_manager = UserManager()
    print("✅ ユーザー管理初期化完了")
    
    # 管理者ユーザー確認
    admin_user = user_manager.authenticate_user('admin', 'admin123')
    if admin_user:
        print("✅ 管理者ユーザー認証テスト成功")
        print(f"   ユーザーID: {admin_user['id']}")
        print(f"   ユーザー名: {admin_user['username']}")
        print(f"   ロール: {admin_user['role']}")
    else:
        print("❌ 管理者ユーザー認証テスト失敗")
    
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()