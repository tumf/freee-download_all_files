# freee 領収書一括ダウンローダ

このプロジェクトは、freee APIを使用して領収書をダウンロードするためのPythonクライアントです。

## セットアップ

### 1. **Poetryのインストール**

   Poetryをインストールしていない場合は、[Poetry公式サイト](https://python-poetry.org/docs/#installation)の指示に従ってインストールしてください。

### 2. **リポジトリのクローンとディレクトリの移動**

```bash
   git clone https://github.com/tumf/freee-download_all_files.git
   cd freee-download_all_files
```

### 3. **依存関係のインストール**

```bash
   poetry install
```

### 4. ** `.env` ファイルの作成と環境変数の設定**

   プロジェクトディレクトリ直下に `.env` ファイルを作成し、以下の環境変数を設定します：

```bash
   FREEE_CLIENT_ID=your_client_id
   FREEE_CLIENT_SECRET=your_client_secret
   COMPANY_ID=your_company_id
   START_DATE=YYYY-MM-DD  # 取得を開始する日付を設定します
```

* `FREEE_CLIENT_ID` と `FREEE_CLIENT_SECRET` は、freee APIアプリケーションの登録時に取得したクレデンシャルを入力してください。
* `COMPANY_ID` は、取得したい領収書が属する事業所のIDを入力してください。
* `START_DATE` は、領収書の取得を開始する日付を `YYYY-MM-DD` 形式で入力してください。例： `2023-01-01`

## 使用方法

### 1. **freee APIの認証**

```bash
   poetry run python freee_oauth_cli.py
```

指示に従ってブラウザで認証を行い、認証コードを入力してください。

### 2. **事業所情報の取得（必要に応じて）**

```bash
   poetry run python get_companies.py
```

取得した `COMPANY_ID` を `.env` ファイルに設定してください。

### 3. **領収書のダウンロード**

```bash
   poetry run python download_receipts.py
```

* プログラムは、 `.env` ファイルで指定した `START_DATE` から現在の日付までを月ごとに区切って領収書を取得・ダウンロードします。
* ダウンロードされた領収書は `downloaded_receipts` ディレクトリに保存されます。
* ファイル名は、 `issue_date_partner_name_receipt_id.extension` の形式で保存されます。

## 注意事項

### **API利用制限**

  APIの利用制限に達しないよう、大量のリクエストを短時間で行わないように注意してください。

#### **拡張子の設定**

  ダウンロードされるファイルの `mime_type` に応じて適切な拡張子が設定されます。必要に応じて `download_receipts.py` 内の `extension_mapping` 辞書に `mime_type` と拡張子のマッピングを追加してください。

## ライセンス

このプロジェクトは [MIT ライセンス](LICENSE) の下で公開されています。
