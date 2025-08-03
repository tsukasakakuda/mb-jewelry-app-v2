# MB Jewelry App - 開発サマリー

## プロジェクト概要
Vue.js 3 + Flask による宝石計算アプリケーション。箱番号グルーピング機能を搭載し、Google Cloud Platform でマルチ環境デプロイメントを実装。

## 現在の状況 (2025-07-20)

### 🔥 本番環境ステータス
- **本番環境 (mb-jewelry-app)**: ❌ 削除済み (コスト削減)
- **ステージング環境 (mb-jewelry-staging)**: ❌ 削除済み (コスト削減)  
- **開発環境 (mb-jewelry-dev)**: ✅ 稼働中
- **ローカル開発環境**: ✅ 稼働中

### 🌿 現在のブランチ
`feature/history-box-edit`

### 📋 完了済み機能
1. ✅ **データベース移行**: JSON ベースから正規化された 3 テーブル構造への完全移行 (users, calculations, calculation_items)
2. ✅ **箱別グルーピング機能**: 履歴固有の箱番号グルーピングとアイテム詳細への遷移機能
3. ✅ **UI 改善**: 
   - 箱別表示を 2 行テーブル形式で全項目表示
   - サイドバーメニューをデスクトップ・モバイルで常時開閉可能に
4. ✅ **商品情報の再構成**:
   - 備考を基本情報欄に移動
   - 詳細情報欄に「LIVE」「RANK」項目を追加
   - 価格情報を新項目で再編成
   - 名称変更: 評価額→地金代金, 素材価格→素材単価
5. ✅ **ナビゲーション改善**: 箱別表示ページから詳細ページへの遷移機能

## 主要実装詳細

### データベース構造 (v3)
```sql
-- ユーザーテーブル
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 計算履歴テーブル
CREATE TABLE calculations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    calculation_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- 計算アイテムテーブル
CREATE TABLE calculation_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    calculation_id INTEGER NOT NULL,
    box_id INTEGER,
    box_no INTEGER,
    material TEXT,
    weight_text TEXT,
    jewelry_price REAL,
    material_price REAL,
    total_weight REAL,
    gemstone_weight REAL,
    material_weight REAL,
    misc TEXT,
    FOREIGN KEY (calculation_id) REFERENCES calculations (id)
);
```

### 変更された重要ファイル
- `backend/calculation_manager_v3.py` - 箱別グルーピングメソッドを含む新データベースマネージャー
- `frontend/src/views/BoxGroupsPage.vue` - アイテム詳細遷移機能付き箱別表示
- `frontend/src/views/ItemDetailPage.vue` - 商品情報レイアウトの再構成
- `frontend/src/components/SidebarMenu.vue` - デスクトップ・モバイル対応の拡張サイドバー

### 箱別グルーピングナビゲーション実装
```javascript
const goToItemDetail = async (entry) => {
  try {
    const response = await axios.get(`/api/calculation-history/${historyId.value}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const items = response.data.calculation_data.items
    let itemIndex = items.findIndex(item => parseInt(item.id) === parseInt(entry.item.id))
    if (itemIndex >= 0) {
      router.push(`/history/${historyId.value}/item/${itemIndex}`)
    }
  } catch (err) {
    console.error('アイテム詳細遷移エラー:', err)
  }
}
```

## デプロイメントインフラ

### Google Cloud Platform 設定
- **プロジェクト**: `mb-jewelry-app` (本番), `mb-jewelry-staging`, `mb-jewelry-dev`
- **サービス**: Google Cloud Run + Cloud SQL PostgreSQL (ステージング・開発)
- **リージョン**: `asia-northeast1` (東京)

### デプロイメントスクリプト
- `deploy.sh` - 本番デプロイメント (SQLite)
- `deploy_staging.sh` - ステージングデプロイメント (Cloud SQL)
- `setup_staging_db.sh` - Cloud SQL インスタンス作成

### GitHub Actions ワークフロー
- `.github/workflows/deploy-production.yml` - main ブランチ自動デプロイ
- `.github/workflows/deploy-staging.yml` - ステージング自動デプロイ
- `.github/workflows/deploy-dev.yml` - 開発環境自動デプロイ

## 環境復旧コマンド

### 本番環境復旧
```bash
# 方法1: 手動デプロイメント
./deploy.sh

# 方法2: GitHub Actions (main ブランチにプッシュ)
git push origin main
```

### ステージング環境復旧
```bash
# 1. Cloud SQL インスタンス再作成
./setup_staging_db.sh

# 2. Cloud Run サービスデプロイ
./deploy_staging.sh

# または GitHub Actions (staging ブランチにプッシュ)
```

### 開発環境確認
```bash
gcloud run services list --project=mb-jewelry-dev --region=asia-northeast1
```

## ローカル開発

### バックエンドコマンド
```bash
cd backend
python app.py  # ポート 5000 で開発サーバー起動
```

### フロントエンドコマンド
```bash
cd frontend
npm run dev    # ポート 5173 で開発サーバー起動
npm run build  # 本番ビルド
```

### データベース操作
```bash
# ローカルデータベース初期化
python init_local_db.py

# 旧スキーマから新スキーマへの移行
python backend/migrate_data_auto.py
```

## プロジェクト構造ハイライト
```
mb-jewelry-app/
├── backend/
│   ├── api.py                    # メイン Flask API (レガシー)
│   ├── api_v3.py                 # v3 データベース対応新 API
│   ├── calculation_manager_v3.py # 新データベースマネージャー
│   ├── migrate_data_auto.py      # 移行スクリプト
│   └── migration_schema.sql      # データベーススキーマ
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   │   ├── BoxGroupsPage.vue      # 箱別グルーピング機能
│   │   │   ├── ItemDetailPage.vue     # 新レイアウトの商品詳細
│   │   │   └── CalculationHistoryPage.vue
│   │   └── components/
│   │       └── SidebarMenu.vue        # 拡張サイドバー
│   └── .env.production           # 本番 API エンドポイント
├── deploy.sh                     # 本番デプロイメント
├── deploy_staging.sh             # ステージングデプロイメント
└── Dockerfile                    # マルチステージ Docker ビルド
```

## 既知の問題と解決策

### Box ID データ型の一貫性
- **問題**: 文字列・整数混在の box_id によるソートエラー
- **解決策**: v3 データベースで INTEGER 型に統一

### 箱別表示からのナビゲーション
- **問題**: goToItemDetail が履歴ページにリダイレクトしていた
- **解決策**: アイテム ID を使用した適切なアイテムインデックス検索の実装

### サイドバーメニューのレスポンシブ対応
- **問題**: デスクトップでメニューにアクセスできない
- **解決策**: 状態管理付きデスクトップトグルボタンの追加

## 次のステップ（再開時）
1. 開発環境での全機能テスト
2. 本番環境復旧タイミングの検討
3. 環境復旧時のクラウドコスト監視
4. 大規模データセット向けデータベース最適化の検討

## コスト管理
- **現在の月額節約**: ~$50-100 (本番 + ステージング削除)
- **開発環境**: ~$10-20/月 (継続開発のため維持)
- **復旧時間**: デプロイスクリプトで約 5-10 分

---
*最終更新: 2025-07-20*  
*現在のブランチ: feature/history-box-edit*  
*本番ステータス: オフライン（コスト削減モード）*