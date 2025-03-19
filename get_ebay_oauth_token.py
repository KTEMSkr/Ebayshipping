import os
import requests
import base64
from dotenv import load_dotenv, set_key

# ✅ .env 파일 로드
load_dotenv()

# ✅ 환경 변수 불러오기
EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
EBAY_REFRESH_TOKEN = os.getenv("EBAY_REFRESH_TOKEN")

if not all([EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_REFRESH_TOKEN]):
    print("❌ eBay API 인증 정보가 없습니다. 환경 변수를 확인하세요.")
    exit(1)

# ✅ Basic Auth를 Base64로 직접 인코딩
auth_string = f"{EBAY_CLIENT_ID}:{EBAY_CLIENT_SECRET}"
auth_encoded = base64.b64encode(auth_string.encode()).decode()

TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {auth_encoded}"
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
