#!/usr/bin/env python3
"""
データベース初期化スクリプト
ユーザーテーブルの作成と初期管理者アカウントの作成を行います
"""

import sqlite3
import hashlib
import bcrypt
from datetime import datetime
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def init_database():
    """データベースとユーザーテーブルを初期化"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # ユーザーテーブル作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # インデックス作成
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_username ON users(username)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_role ON users(role)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_active ON users(is_active)')
    
    conn.commit()
    conn.close()
    print(f"✅ データベースが初期化されました: {DATABASE_PATH}")

def create_admin_user(username='admin', password='admin123', email=None):
    """初期管理者アカウントを作成"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # 既存のユーザーをチェック
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    if cursor.fetchone():
        print(f"⚠️  ユーザー '{username}' は既に存在します")
        conn.close()
        return False
    
    # bcryptでパスワードをハッシュ化
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # ユーザー作成
    cursor.execute('''
        INSERT INTO users (username, password_hash, email, role, is_active, created_at, updated_at)
        VALUES (?, ?, ?, 'admin', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    ''', (username, password_hash, email))
    
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✅ 管理者アカウントを作成しました:")
    print(f"   ユーザー名: {username}")
    print(f"   パスワード: {password}")
    print(f"   ユーザーID: {user_id}")
    return True

def create_regular_user(username='user', password='user123', email=None):
    """一般ユーザーアカウントを作成"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # 既存のユーザーをチェック
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    if cursor.fetchone():
        print(f"⚠️  ユーザー '{username}' は既に存在します")
        conn.close()
        return False
    
    # bcryptでパスワードをハッシュ化
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # ユーザー作成
    cursor.execute('''
        INSERT INTO users (username, password_hash, email, role, is_active, created_at, updated_at)
        VALUES (?, ?, ?, 'user', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    ''', (username, password_hash, email))
    
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✅ 一般ユーザーアカウントを作成しました:")
    print(f"   ユーザー名: {username}")
    print(f"   パスワード: {password}")
    print(f"   ユーザーID: {user_id}")
    return True

def list_users():
    """全ユーザーを表示"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, email, role, is_active, created_at 
        FROM users 
        ORDER BY created_at DESC
    ''')
    
    users = cursor.fetchall()
    conn.close()
    
    if not users:
        print("📝 ユーザーが見つかりません")
        return
    
    print("\n📋 登録ユーザー一覧:")
    print("-" * 80)
    print(f"{'ID':<4} {'ユーザー名':<12} {'メール':<20} {'ロール':<8} {'有効':<6} {'作成日'}")
    print("-" * 80)
    
    for user in users:
        user_id, username, email, role, is_active, created_at = user
        email_display = email or "未設定"
        active_display = "有効" if is_active else "無効"
        created_display = created_at[:16] if created_at else "不明"
        
        print(f"{user_id:<4} {username:<12} {email_display:<20} {role:<8} {active_display:<6} {created_display}")

if __name__ == '__main__':
    print("🚀 MB Jewelry - ユーザーデータベース初期化")
    print("=" * 50)
    
    # データベース初期化
    init_database()
    
    # 初期ユーザー作成
    print("\n👤 初期ユーザーアカウント作成:")
    create_admin_user()
    create_regular_user()
    
    # ユーザー一覧表示
    list_users()
    
    print("\n✨ 初期化完了!")
    print("\n📖 使用方法:")
    print("  - 管理者: admin / admin123")
    print("  - 一般ユーザー: user / user123")