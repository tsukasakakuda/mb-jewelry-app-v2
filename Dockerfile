# フロントエンドビルド用ステージ
FROM node:18 AS build-stage
WORKDIR /app
COPY frontend ./frontend
WORKDIR /app/frontend
RUN npm install && npm run build

# Pythonバックエンドステージ
FROM python:3.9-slim
WORKDIR /app

# ✅ requirements をルートからコピー
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ✅ api.py や他のバックエンドファイルをコピー（users.dbは除外）
COPY backend/*.py ./
COPY backend/*.json ./

# ✅ ビルド済みのフロントを dist にコピー
COPY --from=build-stage /app/frontend/dist ./frontend/dist

# ✅ ポート明示（Cloud Run用）
ENV PORT=8080

# ✅ エントリーポイントをapi.pyに（v3の新しい3テーブル構造対応）
CMD ["python", "api.py"]