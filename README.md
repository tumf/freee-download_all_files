# freee API Client

このプロジェクトは、freee APIを使用して領収書をダウンロードするためのPythonクライアントです。

## セットアップ

1. Poetryをインストールしていない場合は、[Poetry公式サイト](https://python-poetry.org/docs/#installation)の指示に従ってインストールしてください。

2. リポジトリをクローンし、プロジェクトディレクトリに移動します：

```bash
   git clone https://github.com/yourusername/freee-api-client.git
   cd freee-api-client
```

3. Poetry を使用して依存関係をインストールします：

```bash
   poetry install
```

4. `.env` ファイルを作成し、以下の環境変数を設定します：

```bash
FREEE_CLIENT_ID=your_client_id
FREEE_CLIENT_SECRET=your_client_secret
COMPANY_ID=your_company_id
```

## 使用方法

1. freee APIの認証を行います：

```bash
poetry run python freee_oauth_cli.py
```

   指示に従ってブラウザで認証を行い、認証コードを入力してください。

2. 事業所情報を取得します：

```bash
poetry run python get_companies.py
```

3. 領収書をダウンロードします：

```bash
poetry run python download_receipts.py
```

ダウンロードされた領収書は `downloaded_receipts` ディレクトリに保存されます。

## 注意事項

* このスクリプトは、freee APIの利用規約に従って使用してください。
* API利用制限に注意してください。大量のリクエストを短時間で行うと、アカウントがブロックされる可能性があります。

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。
