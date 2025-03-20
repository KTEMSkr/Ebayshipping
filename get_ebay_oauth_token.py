import requests
import base64
import os

# ✅ 환경 변수에서 가져오기
CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")

# ✅ Client ID / Secret이 없으면 에러 발생
if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("❌ ERROR: EBAY_CLIENT_ID 또는 EBAY_CLIENT_SECRET이 설정되지 않음!")

# ✅ eBay OAuth Token 요청 URL
TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

# ✅ Basic 인증을 위한 Base64 인코딩
credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

# ✅ 요청 헤더 및 바디
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {encoded_credentials}"
}
data = {
    "grant_type": "client_credentials",
    "scope": "https://api.ebay.com/oauth/api_scope"
}

# ✅ 요청 실행
response = requests.post(TOKEN_URL, headers=headers, data=data)

# ✅ 응답 확인
if response.status_code == 200:
    token_data = response.json()
    ACCESS_TOKEN = token_data["access_token"]
    print("✔️ eBay OAuth 토큰 발급 성공:", ACCESS_TOKEN)
else:
    print("❌ eBay OAuth 토큰 발급 실패:", response.text)
