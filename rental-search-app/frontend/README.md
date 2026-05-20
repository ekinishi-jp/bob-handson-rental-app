# Rental Search Frontend

賃貸物件検索アプリのReact/Viteフロントエンドです。物件の検索、詳細確認、お気に入り登録、問い合わせ送信をブラウザから操作できます。

## 技術スタック

- React
- Vite
- npm
- lucide-react

## セットアップ

```bash
npm install
npm run dev
```

画面は`http://localhost:5173`で確認できます。

## ビルド

```bash
npm run build
```

ビルド結果は`dist/`に出力されます。

## API接続

デフォルトでは`http://localhost:8000`のバックエンドAPIに接続します。接続先を変更する場合は、環境変数`VITE_API_BASE`を指定します。

```bash
VITE_API_BASE=http://localhost:8000 npm run dev
```

## 主な画面機能

- 検索フォーム: キーワード、駅名、家賃、間取り、駅徒歩で物件を検索
- 検索結果: 物件カード一覧を表示
- 物件詳細: 家賃、所在地、設備、説明文を表示
- お気に入り: 気になる物件をデモユーザーごとに保存
- 問い合わせ: 選択した物件への問い合わせを送信
