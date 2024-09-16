import requests
from freee_oauth_cli import get_access_token


def get_companies():
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}

    url = "https://api.freee.co.jp/api/1/companies"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        companies = response.json()["companies"]
        return companies
    else:
        print(f"エラーが発生しました。ステータスコード: {response.status_code}")
        print(f"エラーメッセージ: {response.text}")
        return None


def display_companies(companies):
    if companies:
        print("事業所一覧:")
        for company in companies:
            print(f"ID: {company['id']}, 名前: {company['display_name']}")
    else:
        print("事業所情報を取得できませんでした。")


if __name__ == "__main__":
    companies = get_companies()
    display_companies(companies)
