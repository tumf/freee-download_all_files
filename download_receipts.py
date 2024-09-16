import os
from datetime import datetime, timedelta

import requests
from dateutil.relativedelta import (
    relativedelta,  # Add relativedelta for monthly increments
)

from freee_oauth_cli import get_access_token

# アクセストークンを取得
ACCESS_TOKEN = get_access_token()

# .envからCOMPANY_IDを取得
COMPANY_ID = os.getenv("COMPANY_ID")

# Add headers definition
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Accept": "application/json"}

# 保存先ディレクトリを作成
save_dir = "downloaded_receipts"
os.makedirs(save_dir, exist_ok=True)

# Set initial start date
start_date = datetime(2023, 12, 1)
current_date = datetime.now()

while start_date < current_date:
    end_date = (start_date + relativedelta(months=1) - timedelta(days=1)).strftime(
        "%Y-%m-%d"
    )
    if datetime.strptime(end_date, "%Y-%m-%d") > current_date:
        end_date = current_date.strftime("%Y-%m-%d")

    # Update receipts_url with current date range
    receipts_url = (
        f"https://api.freee.co.jp/api/1/receipts?"
        f"company_id={COMPANY_ID}&start_date={start_date.strftime('%Y-%m-%d')}"
        f"&end_date={end_date}&limit=3000"
    )
    response = requests.get(receipts_url, headers=headers)

    # レスポンスの構造に基づいてデータを取得
    data = response.json()
    receipts = data.get("receipts", [])

    if not receipts:
        print(
            f"No receipts found for period {start_date.strftime('%Y-%m-%d')} to {end_date}."
        )
        start_date += relativedelta(months=1)
        continue

    # 各領収をダウンロード
    for receipt in receipts:
        print(receipt)
        receipt_id = receipt["id"]
        issue_date = receipt.get("receipt_metadatum", {}).get("issue_date")
        if not issue_date:
            print(
                f"receipt_id {receipt_id} に 'issue_date' がありません。利用可能なキー: {list(receipt.keys())}"
            )
            issue_date = "unknown_date"
        partner_name = receipt.get("receipt_metadatum", {}).get(
            "partner_name", "unknown"
        )
        # Set file extension based on mime_type
        mime_type = receipt.get("mime_type", "application/octet-stream")
        extension_mapping = {
            "application/pdf": "pdf",
            "image/jpeg": "jpg",
            "image/png": "png",
            "image/gif": "gif",
            "text/plain": "txt",
            # Add more mappings as needed
        }
        ext = extension_mapping.get(mime_type, "bin")
        file_name = f"{issue_date}_{partner_name}_{receipt_id}.{ext}"
        # Clean file name
        file_name = "".join(c for c in file_name if c.isalnum() or c in ["_", "-", "."])

        # Check if file already exists, skip if it does
        file_path = os.path.join(save_dir, file_name)
        if os.path.exists(file_path):
            print(f"既にダウンロード済み: {file_name} (スキップ)")
            continue

        # ファイルのダウンロードURLを取得
        download_url = f"https://api.freee.co.jp/api/1/receipts/{receipt_id}/download?company_id={COMPANY_ID}"
        file_response = requests.get(download_url, headers=headers)

        if file_response.status_code == 200:
            # ファイルの保存
            with open(file_path, "wb") as f:
                f.write(file_response.content)
            print(f"ダウンロード完了: {file_name}")
        else:
            # 変更点: エラーの詳細を表示
            print(
                f"ダウンロード失敗: {file_name} "
                f"(ステータスコード: {file_response.status_code}, エラー: {file_response.text})"
            )

    # Move to the next month
    start_date += relativedelta(months=1)

print("すべての領収書のダウンロードが完了しました。")
