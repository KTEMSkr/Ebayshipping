import os
import requests
from requests.auth import HTTPBasicAuth

# eBay OAuth 2.0 엔드포인트
EBAY_OAUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token"

# eBay Orders API 엔드포인트
EBAY_ORDERS_API_URL = "https://api.ebay.com/sell/fulfillment/v1/order"

# GitHub Actions에서 환경 변수 가져오기
EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")  # Client ID
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")  # Client Secret

# ✅ 1️⃣ Access Token 요청
def get_access_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials", "scope": "https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly"}

    response = requests.post(EBAY_OAUTH_URL, headers=headers, data=data, auth=HTTPBasicAuth(EBAY_CLIENT_ID, EBAY_CLIENT_SECRET))

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("✅ OAuth 2.0 Access Token 발급 성공!")
        return access_token
    else:
        print(f"❌ Access Token 발급 실패: {response.status_code}")
        print(response.text)
        exit(1)

# ✅ 2️⃣ 주문 조회 API 호출
def fetch_orders(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",  # OAuth 2.0 토큰 사용!
        "Accept": "application/json"
    }

    params = {
        "limit": 5,  # 최신 5개 주문만 가져오기
        "sort": "-creationDate"
    }

    response = requests.get(EBAY_ORDERS_API_URL, headers=headers, params=params)

    if response.status_code == 200:
        print("✅ 주문 조회 성공!")
        print(response.json())
    else:
        print(f"❌ 주문 조회 실패: {response.status_code}")
        print(response.text)

# ✅ 3️⃣ 실행 (Access Token 받아서 API 호출)
if __name__ == "__main__":
    access_token = get_access_token()  # Access Token 요청
    fetch_orders(access_token)  # eBay 주문 데이터 조회
