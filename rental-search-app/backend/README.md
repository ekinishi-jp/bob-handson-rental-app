# Rental Search Backend

賃貸物件検索アプリのFastAPIバックエンドです。物件検索、物件詳細、問い合わせのAPIを提供します。

## 技術スタック

- Python 3.11+
- FastAPI
- SQLite
- pytest
- uv

## セットアップ

```bash
uv sync
uv run uvicorn app.main:app --reload
```

APIは`http://localhost:8000`で起動します。

## テスト

```bash
uv run pytest
```

## 主なエンドポイント

- `GET /api/health`: ヘルスチェック
- `GET /api/properties`: 物件一覧と検索
- `GET /api/properties/{property_id}`: 物件詳細
- `POST /api/inquiries`: 問い合わせ登録
- `GET /api/inquiries/{inquiry_id}`: 問い合わせ詳細

## デモ用ユーザー

認証は簡易実装として、`X-Demo-User-Id`ヘッダーでユーザーを切り替えます。

```bash
curl -X POST http://localhost:8000/api/inquiries \
  -H "Content-Type: application/json" \
  -H "X-Demo-User-Id: demo-user-1" \
  -d '{"property_id":1,"name":"山田 太郎","email":"taro@example.com","phone":"090-0000-0000","message":"詳細を確認したいです。"}'
```
