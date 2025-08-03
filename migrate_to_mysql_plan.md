# PostgreSQL → MySQL 移行計画

## 移行時間の見積もり
- **開発時間**: 約4-6時間
- **テスト時間**: 約2-3時間
- **リスク**: 中程度（データ移行、構文差異）

## 主な変更点

### 1. Cloud SQLインスタンス
```bash
# 新しいMySQLインスタンス作成
gcloud sql instances create mb-jewelry-mysql \
  --database-version=MYSQL_8_0 \
  --tier=db-f1-micro \
  --region=asia-northeast1
```

### 2. データベース依存関係
```python
# requirements.txt
- psycopg2-binary
+ mysql-connector-python
```

### 3. SQL構文の差異
- `SERIAL` → `AUTO_INCREMENT`
- `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` → `TIMESTAMP DEFAULT CURRENT_TIMESTAMP`
- プレースホルダー `%s` → `%s` (同じ)

### 4. 接続文字列
```python
# PostgreSQL
'postgresql://user:pass@host:5432/db'
# MySQL  
'mysql://user:pass@host:3306/db'
```

## メリット
- Sequel Aceで直接接続可能
- MySQLの豊富なツール群
- 一部のホスティングで安価

## デメリット
- 既存データの移行作業
- 開発時間のロス
- PostgreSQLの高機能を失う