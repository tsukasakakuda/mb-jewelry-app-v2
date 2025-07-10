# MB Jewelry App

ジュエリー業界向けのWEBアプリケーション。CSV処理と地金計算機能を提供します。

## 🚀 機能

- **CSV加工**: ジュエリーデータCSVの編集・変換
- **地金計算**: 素材重量と価格の自動計算
- **重量チェック**: データの重量値検証
- **レスポンシブデザイン**: モバイル・デスクトップ対応

## 🛠️ 技術スタック

- **フロントエンド**: Vue.js 3, Tailwind CSS, Vite
- **バックエンド**: Flask, Pandas, NumPy
- **デプロイ**: Google Cloud Run, Docker
- **CI/CD**: GitHub Actions（予定）

## 📦 セットアップ

### 開発環境

```bash
# リポジトリをクローン
git clone https://github.com/tsukasakakuda/mb-jewelry-app-v2.git
cd mb-jewelry-app-v2

# フロントエンドの準備
cd frontend
npm install
npm run dev

# バックエンドの準備（別ターミナル）
cd backend
pip install -r requirements.txt
python api.py
```

### 本番デプロイ

```bash
# GCPにデプロイ
./deploy.sh YOUR_PROJECT_ID asia-northeast1
```

## 🔧 開発コマンド

```bash
# フロントエンド開発サーバー
cd frontend && npm run dev

# フロントエンドビルド
cd frontend && npm run build

# バックエンドサーバー
cd backend && python api.py
```

## 🌐 本番環境

現在のデプロイ先: https://mb-jewelry-app-x4vd6r3wqq-an.a.run.app

## 📝 ライセンス

Private Project