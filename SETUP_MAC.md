# Mac 環境セットアップ手順

この手順書は、macOS の参加者が賃貸物件検索モックアプリを起動するための準備手順です。

## 1. 前提

使用するもの:

- macOS
- Terminal
- Webブラウザ
- Bob
- インターネット接続

配布アセットには、以下の生成物は含めない想定です。

- `rental-search-app/backend/rental.db`
- `rental-search-app/backend/.venv`
- `rental-search-app/frontend/node_modules`
- `rental-search-app/frontend/dist`

これらは参加者のMac上でセットアップ・起動時に作成されます。

## 2. 必要なツール

このハンズオンでは以下を使用します。

- `uv`: Pythonプロジェクトの依存関係管理と実行
- Python 3.12: Backend APIの実行環境
- Node.js: Reactアプリの実行環境
- `npm`: Reactアプリの依存関係管理
- React 19: Frontend UIの実装ライブラリ

Python本体は、`uv`が必要に応じて検出または取得できます。そのため、まずは`uv`が動作する状態にすることを優先します。

## 3. 事前準備 - インストール済みか確認

Terminalを開き、以下を実行します。

```bash
uv --version
node -v
npm -v
```

すべてバージョンが表示されれば、必要な実行環境は概ね揃っています。

例:

```text
uv 0.x.x
v22.x.x
10.x.x
```

いずれかが `command not found` になる場合は、次の手順でインストールしてください。

## 4. 事前準備 - uv のインストール

### 方法A: Homebrewを使う

Homebrewが利用できるMacでは、以下でインストールできます。

```bash
brew install uv
```

インストール後、確認します。

```bash
uv --version
```

### 方法B: 公式インストーラーを使う

Terminalで以下を実行します。

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

インストール後、Terminalを開き直して確認します。

```bash
uv --version
```

## 5. 事前準備 - Python の確認

Pythonがまだ入っていない場合でも問題ありません。
この手順では、`uv` を使って必要なPythonをインストールできます。

この手順ではPython 3.12を使用します。プロジェクト設定上はPython 3.11以上に対応していますが、ハンズオンでは3.12で統一します。

`uv`で利用可能なPythonを確認します。

```bash
uv python list
```

Python 3.12が見つからない場合や、明示的にインストールしたい場合は以下を実行します。

```bash
uv python install 3.12
```

## 6. 事前準備 - Node.js / npm のインストール

`node -v`または`npm -v`が動かない場合は、Node.jsをインストールします。npmはNode.jsに同梱されています。

### 方法A: Homebrewを使う

Homebrewが利用できるMacでは、以下でインストールできます。

```bash
brew install node
```

インストール後、確認します。

```bash
node -v
npm -v
```

### 方法B: Node.js公式インストーラーを使う

1. ブラウザで以下を開きます。
   - https://nodejs.org/
2. `LTS`版のmacOS Installerをダウンロードします。
3. インストーラーを実行し、画面の指示に従ってインストールします。
4. Terminalを開き直して確認します。

```bash
node -v
npm -v
```

### 方法C: Node version managerを使う

すでに `fnm`、`nvm`、`volta` などを使っている場合は、それらでNode.js LTS版をインストールしても問題ありません。

例:

```bash
fnm install --lts
fnm use --lts
```

---

**事前準備はここまでです。以下は当日行います。**

---

## 7. ハンズオン資材の配置

配布された `bob-handson-app-python-javascript` フォルダを任意の場所に展開します。

例:

```text
/Users/<ユーザー名>/Desktop/bob-handson-app-python-javascript
```

Terminalでそのフォルダへ移動します。

```bash
cd /Users/<ユーザー名>/Desktop/bob-handson-app-python-javascript
```

## 8. Backend の起動

Terminalを1つ開き、以下を実行します。

```bash
cd rental-search-app/backend
uv sync
uv run uvicorn app.main:app --reload
```

以下のような表示が出ればBackendは起動しています。

```text
Uvicorn running on http://127.0.0.1:8000
```

このTerminalは閉じずに、そのままにしてください。

## 9. Frontend の起動

別のTerminalを開き、配布フォルダへ移動してから以下を実行します。

```bash
cd rental-search-app/frontend
npm install
npm run dev
```

以下のような表示が出ればFrontendは起動しています。

```text
Local: http://localhost:5173/
```

このTerminalも閉じずに、そのままにしてください。

## 10. 動作確認

ブラウザで以下を開きます。

```text
http://localhost:5173
```

以下を確認します。

- 賃貸物件検索画面が表示される
- 検索結果が表示される
- 物件詳細が表示される
- 問い合わせフォームが表示される

Backend APIの疎通確認をする場合は、以下も開けます。

```text
http://localhost:8000/api/health
```

以下が表示されればBackendは動作しています。

```json
{"status":"ok"}
```

## 11. アプリの停止

Backendを起動しているTerminalで `Ctrl + C` を押します。

Frontendを起動しているTerminalでも `Ctrl + C` を押します。

## 12. DBを初期化する

問い合わせやお気に入りなど、ハンズオン中に登録したデータを消して初期状態に戻す場合は、配布フォルダ直下で以下を実行します。

```bash
rm -f rental-search-app/backend/rental.db
```

次回Backendを起動すると、初期物件データ100件が自動で再作成されます。

## 13. 依存関係や生成物も削除する

Mac上の容量を戻したい場合は、以下を削除できます。

```bash
rm -rf rental-search-app/backend/.venv
rm -rf rental-search-app/frontend/node_modules
rm -rf rental-search-app/frontend/dist
```

これらを削除しても、次回 `uv sync` や `npm install` を実行すれば再作成されます。

## 14. よくあるトラブル

### `uv`、`node`、`npm` が見つからない

インストール後にTerminalを開き直してください。改善しない場合は、Macを再起動してください。

### `npm install` が失敗する

会社PCのプロキシやセキュリティ設定により、npmレジストリへアクセスできない場合があります。社内ネットワーク設定を確認してください。

### `uv sync` が失敗する

会社PCのプロキシやセキュリティ設定により、Pythonパッケージの取得に失敗している可能性があります。社内ネットワーク設定を確認してください。

### ポートが使用中と表示される

Backendは`8000`、Frontendは`5173`を使用します。以前起動したプロセスが残っている場合は、該当するTerminalで `Ctrl + C` して停止してください。

### Apple Silicon / Intel Mac の違いが気になる

このハンズオンでは通常、手順を分ける必要はありません。`uv`、Node.js、npmはいずれもmacOS向けに配布されており、Homebrewまたはインストーラーが環境に合うものを導入します。

### 画面が開けない

BackendとFrontendの両方が起動しているか確認してください。Frontendだけ起動していても、Backendが止まっているとAPI通信に失敗します。
