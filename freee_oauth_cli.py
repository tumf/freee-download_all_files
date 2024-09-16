from requests_oauthlib import OAuth2Session
import webbrowser
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

# freee API credentials
CLIENT_ID = os.getenv("FREEE_CLIENT_ID")
CLIENT_SECRET = os.getenv("FREEE_CLIENT_SECRET")
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"

# freee OAuth endpoints
AUTHORIZATION_BASE_URL = "https://accounts.secure.freee.co.jp/public_api/authorize"
TOKEN_URL = "https://accounts.secure.freee.co.jp/public_api/token"

# トークンを保存するファイル
TOKEN_FILE = "freee_token.json"


def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        json.dump(token, f)


def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None


def get_new_token():
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError(
            "CLIENT_ID または CLIENT_SECRET が設定されていません。.envファイルを確認してください。"
        )

    freee = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    authorization_url, _ = freee.authorization_url(AUTHORIZATION_BASE_URL)

    print(f"以下のURLをブラウザで開いて認証を行ってください：\n{authorization_url}")
    webbrowser.open(authorization_url)

    auth_code = input("認証コードを入力してください: ")

    token = freee.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, code=auth_code)
    save_token(token)
    return token


def refresh_token(token):
    extra = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    freee = OAuth2Session(CLIENT_ID, token=token)
    new_token = freee.refresh_token(TOKEN_URL, **extra)
    save_token(new_token)
    return new_token


def get_access_token():
    token = load_token()
    if token:
        # freee = OAuth2Session(CLIENT_ID, token=token)
        if token.get("expires_at") and token["expires_at"] < time.time():
            token = refresh_token(token)
    else:
        token = get_new_token()

    return token["access_token"]


if __name__ == "__main__":
    access_token = get_access_token()
    print(f"アクセストークン: {access_token}")
