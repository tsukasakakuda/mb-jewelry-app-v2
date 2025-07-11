"""
ユーザー管理モジュール
データベースを使用したユーザー認証と管理機能を提供
"""

import sqlite3
import bcrypt
import os
from datetime import datetime
from typing import Optional, Dict, List

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

class UserManager:
    """ユーザー管理クラス"""
    
    def __init__(self):
        self.db_path = DATABASE_PATH
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        """データベースファイルの存在確認"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"データベースファイルが見つかりません: {self.db_path}")
    
    def _get_connection(self):
        """データベース接続を取得"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 辞書形式でアクセス可能
        return conn
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """
        ユーザー認証
        
        Args:
            username: ユーザー名
            password: パスワード
            
        Returns:
            認証成功時はユーザー情報辞書、失敗時はNone
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # ユーザー検索
            cursor.execute('''
                SELECT id, username, password_hash, email, role, is_active
                FROM users 
                WHERE username = ? AND is_active = 1
            ''', (username,))
            
            user = cursor.fetchone()
            if not user:
                return None
            
            # パスワード照合
            if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                # ログイン成功時は最終ログイン時刻を更新
                cursor.execute('''
                    UPDATE users 
                    SET updated_at = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (user['id'],))
                conn.commit()
                
                # パスワードハッシュを除外してユーザー情報を返す
                return {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role'],
                    'is_active': user['is_active']
                }
            
            return None
            
        except Exception as e:
            print(f"認証エラー: {e}")
            return None
        finally:
            conn.close()
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """
        ユーザーIDでユーザー情報を取得
        
        Args:
            user_id: ユーザーID
            
        Returns:
            ユーザー情報辞書またはNone
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, username, email, role, is_active, created_at, updated_at
                FROM users 
                WHERE id = ?
            ''', (user_id,))
            
            user = cursor.fetchone()
            if user:
                return dict(user)
            return None
            
        except Exception as e:
            print(f"ユーザー取得エラー: {e}")
            return None
        finally:
            conn.close()
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """
        ユーザー名でユーザー情報を取得
        
        Args:
            username: ユーザー名
            
        Returns:
            ユーザー情報辞書またはNone
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, username, email, role, is_active, created_at, updated_at
                FROM users 
                WHERE username = ?
            ''', (username,))
            
            user = cursor.fetchone()
            if user:
                return dict(user)
            return None
            
        except Exception as e:
            print(f"ユーザー取得エラー: {e}")
            return None
        finally:
            conn.close()
    
    def create_user(self, username: str, password: str, email: str = None, 
                   role: str = 'user') -> Optional[int]:
        """
        新しいユーザーを作成
        
        Args:
            username: ユーザー名
            password: パスワード
            email: メールアドレス
            role: ユーザーロール
            
        Returns:
            作成されたユーザーIDまたはNone
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # ユーザー名の重複チェック
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                print(f"ユーザー名 '{username}' は既に使用されています")
                return None
            
            # パスワードをハッシュ化
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # ユーザー作成
            cursor.execute('''
                INSERT INTO users (username, password_hash, email, role, is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ''', (username, password_hash, email, role))
            
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
            
        except Exception as e:
            print(f"ユーザー作成エラー: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def update_password(self, user_id: int, new_password: str) -> bool:
        """
        ユーザーのパスワードを更新
        
        Args:
            user_id: ユーザーID
            new_password: 新しいパスワード
            
        Returns:
            更新成功時True、失敗時False
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # パスワードをハッシュ化
            password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # パスワード更新
            cursor.execute('''
                UPDATE users 
                SET password_hash = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (password_hash, user_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                return True
            
            return False
            
        except Exception as e:
            print(f"パスワード更新エラー: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def deactivate_user(self, user_id: int) -> bool:
        """
        ユーザーを無効化
        
        Args:
            user_id: ユーザーID
            
        Returns:
            無効化成功時True、失敗時False
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users 
                SET is_active = 0, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (user_id,))
            
            if cursor.rowcount > 0:
                conn.commit()
                return True
            
            return False
            
        except Exception as e:
            print(f"ユーザー無効化エラー: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def list_users(self, active_only: bool = True) -> List[Dict]:
        """
        ユーザー一覧を取得
        
        Args:
            active_only: 有効なユーザーのみ取得するか
            
        Returns:
            ユーザー情報のリスト
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            if active_only:
                cursor.execute('''
                    SELECT id, username, email, role, is_active, created_at, updated_at
                    FROM users 
                    WHERE is_active = 1
                    ORDER BY created_at DESC
                ''')
            else:
                cursor.execute('''
                    SELECT id, username, email, role, is_active, created_at, updated_at
                    FROM users 
                    ORDER BY created_at DESC
                ''')
            
            users = cursor.fetchall()
            return [dict(user) for user in users]
            
        except Exception as e:
            print(f"ユーザー一覧取得エラー: {e}")
            return []
        finally:
            conn.close()

# シングルトンインスタンス
user_manager = UserManager()