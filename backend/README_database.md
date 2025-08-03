# データベース認証システム

## 概要

MB Jewelry アプリケーションは、SQLiteデータベースを使用してユーザー認証とアカウント管理を行います。

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. データベースの初期化

```bash
python3 init_db.py
```

このコマンドで以下が実行されます：
- SQLiteデータベース `users.db` の作成
- ユーザーテーブルの作成
- 初期管理者アカウントの作成
- 初期一般ユーザーアカウントの作成

### 3. 初期アカウント

データベース初期化後、以下のアカウントが使用可能です：

**管理者アカウント:**
- ユーザー名: `admin`
- パスワード: `admin123`
- ロール: `admin`

**一般ユーザーアカウント:**
- ユーザー名: `user`
- パスワード: `user123`
- ロール: `user`

## データベース構造

### users テーブル

| カラム名      | データ型  | 説明                |
|---------------|-----------|---------------------|
| id            | INTEGER   | ユーザーID (主キー) |
| username      | TEXT      | ユーザー名 (一意)   |
| password_hash | TEXT      | パスワードハッシュ  |
| email         | TEXT      | メールアドレス      |
| role          | TEXT      | ユーザーロール      |
| is_active     | BOOLEAN   | アカウント有効状態  |
| created_at    | DATETIME  | 作成日時            |
| updated_at    | DATETIME  | 更新日時            |

## API エンドポイント

### 認証

#### ログイン
```http
POST /api/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

#### レスポンス（成功）
```json
{
  "token": "eyJ...",
  "message": "ログインに成功しました",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

### ユーザー管理

#### ユーザー情報取得
```http
GET /api/user/profile
Authorization: Bearer <token>
```

#### パスワード変更
```http
POST /api/user/change-password
Authorization: Bearer <token>
Content-Type: application/json

{
  "current_password": "現在のパスワード",
  "new_password": "新しいパスワード"
}
```

### 管理者機能

#### ユーザー一覧取得（管理者のみ）
```http
GET /api/admin/users
Authorization: Bearer <admin_token>
```

#### ユーザー作成（管理者のみ）
```http
POST /api/admin/users
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "username": "新しいユーザー名",
  "password": "パスワード",
  "email": "email@example.com",
  "role": "user"
}
```

## セキュリティ機能

### パスワードハッシュ化
- **bcrypt** を使用してパスワードを安全にハッシュ化
- ソルト付きハッシュでレインボーテーブル攻撃を防止

### JWT トークン
- JSON Web Token を使用した状態を持たない認証
- トークンにユーザーID、ユーザー名、ロールを含む
- 1時間の有効期限

### ロールベースアクセス制御
- `admin`: 全機能にアクセス可能
- `user`: 一般機能のみアクセス可能

## データベース管理

### ユーザー一覧表示
```bash
python3 init_db.py
```

### SQLite直接アクセス
```bash
sqlite3 users.db
.tables
SELECT * FROM users;
```

### バックアップ
```bash
cp users.db users_backup_$(date +%Y%m%d_%H%M%S).db
```

## トラブルシューティング

### データベースファイルが見つからない
```bash
python3 init_db.py
```

### パスワード忘れの場合
管理者アカウントでログインして新しいユーザーを作成するか、データベースを再初期化してください。

### 権限エラー
- トークンが正しく設定されているか確認
- トークンの有効期限が切れていないか確認
- ユーザーロールが適切か確認

## 旧システムからの移行

従来のハードコーディングされたユーザー辞書は削除され、データベースベースの認証に移行されました。既存のユーザー名とパスワードは以下のように対応します：

- `admin` / `admin123` → データベース内の管理者アカウント
- `user` / `user123` → データベース内の一般ユーザーアカウント

フロントエンドのログイン機能は変更なしで動作します。