# Rental Search

賃貸物件を検索し、詳細確認、お気に入り登録、問い合わせ送信ができるデモアプリケーションです。

## 概要

Rental Searchは、物件情報を条件で絞り込み、気になる物件の詳細を確認できる賃貸検索アプリです。フロントエンドはReact、バックエンドはFastAPIで構成されています。

## 主な機能

- 物件検索: キーワード、駅名、上限家賃、間取り、駅徒歩で絞り込み
- 物件詳細: 家賃、管理費、敷金礼金、設備、所在地などを表示
- お気に入り: デモユーザーごとに物件を保存
- 問い合わせ: 物件に対する問い合わせ内容を登録

## 技術スタック

- Backend: Python 3.11+, FastAPI, SQLite, pytest, uv
- Frontend: React, Vite, npm

## ディレクトリ構成

```text
.
├── backend/   # FastAPI APIとSQLiteデータベース
└── frontend/  # React/Viteフロントエンド
```

## セットアップ

### Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

APIは`http://localhost:8000`で起動します。

### Frontend

```bash
cd frontend
npm install
npm run dev
```

画面は`http://localhost:5173`で確認できます。

## API

バックエンドは以下のAPIを提供します。

- `GET /api/health`
- `GET /api/properties`
- `GET /api/properties/{property_id}`
- `GET /api/favorites`
- `POST /api/favorites`
- `POST /api/inquiries`
- `GET /api/inquiries/{inquiry_id}`

お気に入りと問い合わせは、`X-Demo-User-Id`ヘッダーでデモユーザーを切り替えられます。
