import requests
import os
import base64

# ✅ 환경 변수에서 eBay API 키 가져오기
CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("❌ ERROR: `EBAY_CLIENT_ID` 또는 `EBAY_CLIENT_SECRET`이 설정되지 않았습니다!")

# ✅ eBay OAuth 토큰 요청 URL
TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

# ✅ Basic Auth 헤더 생성
auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

headers = {
    "Authorization": f"Basic {auth_header}",
    "Content-Type": "application/x-www-form-urlencoded"
}

# ✅ 🚀 Scope 추가: `sell.fulfillment.readonly`, `sell.fulfillment.readwrite`
data = {
    "grant_type": "client_credentials",
    "scope": "https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly https://api.ebay.com/oauth/api_scope/sell.fulfillment.readwrite"
}

# ✅ eBay OAuth 토큰 요청
response = requests.post(TOKEN_URL, headers=headers, data=data)

if response.status_code == 200:
    token_info = response.json()
    access_token = token_info["access_token"]
    expires_in = token_info["expires_in"]

    print(f"✅ eBay OAuth 토큰 발급 성공: {access_token[:10]}********** (유효 기간: {expires_in}초)")

    # ✅ GitHub Actions에서 사용하려면 환경 변수로 저장
    print(f"::set-output name=ebay_token::{access_token}")

else:
    print("❌ eBay OAuth 토큰 발급 실패:", response.json())
