import os
import requests
from dotenv import load_dotenv, set_key

# ✅ .env 파일 로드
load_dotenv()

# ✅ 환경 변수 불러오기
EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
EBAY_REFRESH_TOKEN = os.getenv("EBAY_REFRESH_TOKEN")

TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {requests.auth._basic_auth_str(EBAY_CLIENT_ID, EBAY_CLIENT_SECRET)}"
}

data = {
    "grant_type": "refresh_token",
    "refresh_token": EBAY_REFRESH_TOKEN,
    "scope": "https://api.ebay.com/oauth/api_scope"
}

response = requests.post(TOKEN_URL, headers=headers, data=data)

if response.status_code == 200:
    new_access_token = response.json().get("access_token")
    print("✅ eBay Access Token 갱신 완료!")

    # ✅ .env 파일에 새 토큰 저장
    set_key(".env", "EBAY_USER_TOKEN", new_access_token)

    print("🔹 새로운 토큰이 .env 파일에 저장되었습니다.")
else:
    print(f"❌ Access Token 갱신 실패: {response.text}")
