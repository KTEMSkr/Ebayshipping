import requests
import os
import base64

# GitHub Secrets에서 Client ID, Client Secret 가져오기
EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")

# Base64 인코딩 (Client ID:Client Secret)
credentials = f"{EBAY_CLIENT_ID}:{EBAY_CLIENT_SECRET}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

# OAuth 토큰 요청
url = "https://api.ebay.com/identity/v1/oauth2/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {encoded_credentials}",
}
body = {
    "grant_type": "client_credentials",
    "scope": "https://api.ebay.com/oauth/api_scope"
}

response = requests.post(url, headers=headers, data=body)

if response.status_code == 200:
    token_data = response.json()
    ACCESS_TOKEN = token_data["access_token"]
    print(f"✅ eBay OAuth 토큰 발급 성공: {ACCESS_TOKEN}")
else:
    print(f"❌ eBay OAuth 토큰 발급 실패: {response.text}")
