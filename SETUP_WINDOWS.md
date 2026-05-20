# Windows 環境セットアップ手順

この手順書は、Windows 10/11 の参加者が賃貸物件検索モックアプリを起動するための準備手順です。

## 1. 前提

使用するもの:

- Windows 10 または Windows 11
- PowerShell
- Webブラウザ
- Bob
- インターネット接続

配布アセットには、以下の生成物は含めない想定です。

- `rental-search-app/backend/rental.db`
- `rental-search-app/backend/.venv`
- `rental-search-app/frontend/node_modules`
- `rental-search-app/frontend/dist`

これらは参加者のPC上でセットアップ・起動時に作成されます。

## 2. 必要なツール

このハンズオンでは以下を使用します。

- `uv`: Pythonプロジェクトの依存関係管理と実行
- Python 3.12: Backend APIの実行環境
- Node.js: Reactアプリの実行環境
- `npm`: Reactアプリの依存関係管理
- React 19: Frontend UIの実装ライブラリ

Python本体は、`uv`が必要に応じて検出または取得できます。そのため、まずは`uv`が動作する状態にすることを優先します。

## 3. 事前準備 - インストール済みか確認

PowerShellを開き、以下を実行します。

```powershell
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

いずれかが「認識されません」などのエラーになる場合は、次の手順でインストールしてください。

## 4. 事前準備 - uv のインストール

### 方法A: WinGetを使う

WinGetが利用できるPCでは、以下でインストールできます。

```powershell
winget install --id=astral-sh.uv -e
```

インストール後、PowerShellを開き直して確認します。

```powershell
uv --version
```

### 方法B: 公式インストーラーを使う

PowerShellで以下を実行します。

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

インストール後、PowerShellを開き直して確認します。

```powershell
uv --version
```

## 5. 事前準備 - Python の確認

Pythonがまだ入っていない場合でも問題ありません。
この手順では、`uv` を使って必要なPythonをインストールできます。

この手順ではPython 3.12を使用します。プロジェクト設定上はPython 3.11以上に対応していますが、ハンズオンでは3.12で統一します。

`uv`で利用可能なPythonを確認します。

```powershell
uv python list
```

Python 3.12が見つからない場合や、明示的にインストールしたい場合は以下を実行します。

```powershell
uv python install 3.12
```

## 6. 事前準備 - Node.js / npm のインストール

`node -v`または`npm -v`が動かない場合は、Node.jsをインストールします。npmはNode.jsに同梱されています。

### 方法A: WinGetを使う

```powershell
winget install OpenJS.NodeJS.LTS
```

インストール後、PowerShellを開き直して確認します。

```powershell
node -v
npm -v
```

### 方法B: Node.js公式インストーラーを使う

1. ブラウザで以下を開きます。
   - https://nodejs.org/
2. `LTS`版のWindows Installerをダウンロードします。
3. インストーラーを実行し、画面の指示に従ってインストールします。
4. PowerShellを開き直して確認します。

```powershell
node -v
npm -v
```

公式インストール手順の参考記事：https://qiita.com/ryosuke_tsuda/items/e31efc789b1f1e544524

---

**事前準備はここまでです。以下は当日行います。**

---

## 7. ハンズオン資材の配置

配布された `bob-handson-app-python-javascript` フォルダを任意の場所に展開します。

例:

```text
C:\Users\<ユーザー名>\Desktop\bob-handson-app-python-javascript
```

PowerShellでそのフォルダへ移動します。

```powershell
cd C:\Users\<ユーザー名>\Desktop\bob-handson-app-python-javascript
```

## 8. Backend の起動

PowerShellを1つ開き、以下を実行します。

```powershell
cd rental-search-app/backend
uv sync
uv run uvicorn app.main:app --reload
```

以下のような表示が出ればBackendは起動しています。

```text
Uvicorn running on http://127.0.0.1:8000
```

このPowerShellは閉じずに、そのままにしてください。

## 9. Frontend の起動

別のPowerShellを開き、配布フォルダへ移動してから以下を実行します。

```powershell
cd rental-search-app/frontend
npm install
npm run dev
```

以下のような表示が出ればFrontendは起動しています。

```text
Local: http://localhost:5173/
```

このPowerShellも閉じずに、そのままにしてください。

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

Backendを起動しているPowerShellで `Ctrl + C` を押します。

Frontendを起動しているPowerShellでも `Ctrl + C` を押します。

## 12. DBを初期化する

問い合わせやお気に入りなど、ハンズオン中に登録したデータを消して初期状態に戻す場合は、配布フォルダ直下で以下を実行します。

```powershell
Remove-Item rental-search-app/backend/rental.db -ErrorAction SilentlyContinue
```

次回Backendを起動すると、初期物件データ100件が自動で再作成されます。

## 13. 依存関係や生成物も削除する

PC上の容量を戻したい場合は、以下を削除できます。

```powershell
Remove-Item rental-search-app/backend/.venv -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item rental-search-app/frontend/node_modules -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item rental-search-app/frontend/dist -Recurse -Force -ErrorAction SilentlyContinue
```

これらを削除しても、次回 `uv sync` や `npm install` を実行すれば再作成されます。

## 14. よくあるトラブル

### `uv`、`node`、`npm` が認識されない

インストール後にPowerShellを開き直してください。改善しない場合は、PCを再起動してください。

### `npm install` が失敗する

会社PCのプロキシやセキュリティ設定により、npmレジストリへアクセスできない場合があります。社内ネットワーク設定を確認してください。

### `uv sync` が失敗する

会社PCのプロキシやセキュリティ設定により、Pythonパッケージの取得に失敗している可能性があります。社内ネットワーク設定を確認してください。

### ポートが使用中と表示される

Backendは`8000`、Frontendは`5173`を使用します。以前起動したプロセスが残っている場合は、該当するPowerShellで `Ctrl + C` して停止してください。

### 画面が開けない

BackendとFrontendの両方が起動しているか確認してください。Frontendだけ起動していても、Backendが止まっているとAPI通信に失敗します。
