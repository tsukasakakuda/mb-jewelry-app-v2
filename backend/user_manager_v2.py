"""
ユーザー管理モジュール v2
db_manager を使用した Cloud SQL 対応版
"""

import bcrypt
import os
from datetime import datetime
from typing import Optional, Dict, List
from db_manager import db_manager

class UserManager:
    """ユーザー管理クラス（Cloud SQL対応）"""
    
    def __init__(self):
        self.db = db_manager
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        """データベーステーブルの存在確認と自動作成"""
        try:
            print("🔧 データベーステーブル初期化中...")
            self.db.initialize_tables()
            print("✅ テーブル初期化完了")
            
            print("👤 デフォルト管理者ユーザー作成中...")
            self._create_default_admin()
            print("✅ ユーザー管理初期化完了")
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
            import traceback
            traceback.print_exc()
    
    def _create_default_admin(self):
        """デフォルト管理者ユーザーの作成"""
        admin_username = 'admin'
        
        # 既存のadminユーザーをチェック
        placeholder = self.db.get_sql_placeholder()
        existing_admin = self.db.execute_query(
            f"SELECT id FROM users WHERE username = {placeholder}",
            (admin_username,)
        )
        
        if not existing_admin:
            admin_password = 'admin123'
            password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
            
            if self.db.db_type == 'postgresql':
                query = f"INSERT INTO users (username, password_hash, role) VALUES ({placeholder}, {placeholder}, {placeholder}) RETURNING id"
            else:
                query = f"INSERT INTO users (username, password_hash, role) VALUES ({placeholder}, {placeholder}, {placeholder})"
            
            admin_id = self.db.execute_insert(
                query,
                (admin_username, password_hash.decode('utf-8'), 'admin')
            )
            
            if admin_id:
                print(f"✅ デフォルト管理者ユーザーを作成しました (ID: {admin_id})")
                print(f"   ユーザー名: {admin_username}")
                print(f"   パスワード: {admin_password}")
    
    def create_user(self, username: str, password: str, role: str = 'user') -> Optional[int]:
        """新しいユーザーを作成"""
        try:
            # ユーザー名の重複チェック
            placeholder = self.db.get_sql_placeholder()
            existing_user = self.db.execute_query(
                f"SELECT id FROM users WHERE username = {placeholder}",
                (username,)
            )
            
            if existing_user:
                print(f"⚠️ ユーザー名 '{username}' は既に存在します")
                return None
            
            # パスワードハッシュ化
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # ユーザー作成
            if self.db.db_type == 'postgresql':
                query = f"INSERT INTO users (username, password_hash, role) VALUES ({placeholder}, {placeholder}, {placeholder}) RETURNING id"
            else:
                query = f"INSERT INTO users (username, password_hash, role) VALUES ({placeholder}, {placeholder}, {placeholder})"
            
            user_id = self.db.execute_insert(
                query,
                (username, password_hash.decode('utf-8'), role)
            )
            
            if user_id:
                print(f"✅ ユーザーを作成しました (ID: {user_id}, ユーザー名: {username}, 役割: {role})")
                return user_id
            
            return None
            
        except Exception as e:
            print(f"ユーザー作成エラー: {e}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """ユーザー認証"""
        try:
            placeholder = self.db.get_sql_placeholder()
            users = self.db.execute_query(
                f"SELECT id, username, password_hash, role FROM users WHERE username = {placeholder}",
                (username,)
            )
            
            if not users:
                print(f"⚠️ ユーザー '{username}' が見つかりません")
                return None
            
            user = users[0]
            password_hash = user['password_hash']
            
            # パスワード検証
            if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
                print(f"✅ ユーザー '{username}' の認証に成功しました")
                return {
                    'id': user['id'],
                    'username': user['username'],
                    'role': user['role']
                }
            else:
                print(f"⚠️ ユーザー '{username}' のパスワードが間違っています")
                return None
                
        except Exception as e:
            print(f"ユーザー認証エラー: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """ユーザーIDでユーザー情報を取得"""
        try:
            placeholder = self.db.get_sql_placeholder()
            users = self.db.execute_query(
                f"SELECT id, username, role, created_at FROM users WHERE id = {placeholder}",
                (user_id,)
            )
            
            if users:
                return dict(users[0])
            return None
            
        except Exception as e:
            print(f"ユーザー取得エラー: {e}")
            return None
    
    def get_all_users(self) -> List[Dict]:
        """全ユーザーリストを取得"""
        try:
            users = self.db.execute_query(
                "SELECT id, username, role, created_at FROM users ORDER BY created_at DESC"
            )
            
            return [dict(user) for user in users] if users else []
            
        except Exception as e:
            print(f"ユーザーリスト取得エラー: {e}")
            return []
    
    def update_user_role(self, user_id: int, new_role: str) -> bool:
        """ユーザーの役割を更新"""
        try:
            placeholder = self.db.get_sql_placeholder()
            affected_rows = self.db.execute_query(
                f"UPDATE users SET role = {placeholder} WHERE id = {placeholder}",
                (new_role, user_id)
            )
            
            if affected_rows > 0:
                print(f"✅ ユーザー（ID: {user_id}）の役割を '{new_role}' に更新しました")
                return True
            
            return False
            
        except Exception as e:
            print(f"ユーザー役割更新エラー: {e}")
            return False
    
    def delete_user(self, user_id: int) -> bool:
        """ユーザーを削除"""
        try:
            placeholder = self.db.get_sql_placeholder()
            affected_rows = self.db.execute_query(
                f"DELETE FROM users WHERE id = {placeholder}",
                (user_id,)
            )
            
            if affected_rows > 0:
                print(f"✅ ユーザー（ID: {user_id}）を削除しました")
                return True
            
            return False
            
        except Exception as e:
            print(f"ユーザー削除エラー: {e}")
            return False