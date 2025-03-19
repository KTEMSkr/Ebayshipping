import requests
import os

# 🔹 eBay API 요청 URL (주문 목록 가져오기)
EBAY_API_URL = "https://api.ebay.com/sell/fulfillment/v1/order?limit=50"

def refresh_ebay_user_token():
    """eBay User Token을 갱신하는 함수"""
    EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
    EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
    EBAY_REFRESH_TOKEN = os.getenv("EBAY_USER_TOKEN")  # 갱신용 토큰

    if not all([EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_REFRESH_TOKEN]):
        print("❌ eBay API 인증 정보가 없습니다.")
        return None

    # 🔹 eBay OAuth 토큰 요청 URL
    TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

    # 🔹 요청 헤더
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {requests.auth._basic_auth_str(EBAY_CLIENT_ID, EBAY_CLIENT_SECRET)}"
    }

    # 🔹 요청 데이터
    data = {
        "grant_type": "refresh_token",
        "refresh_token": EBAY_REFRESH_TOKEN,
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    # 🔹 eBay API 호출 (토큰 갱신)
    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code == 200:
        new_access_token = response.json().get("access_token")
        print("✅ eBay Access Token 갱신 완료!")
        return new_access_token
    else:
        print(f"❌ Access Token 갱신 실패: {response.text}")
        return None

# ✅ 갱신된 Access Token 가져오기
ACCESS_TOKEN = refresh_ebay_user_token()

if ACCESS_TOKEN:
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    # ✅ eBay API에서 주문 목록 가져오기
    response = requests.get(EBAY_API_URL, headers=headers)

    if response.status_code == 200:
        orders = response.json().get("orders", [])
        print(f"✅ {len(orders)}개의 주문을 가져왔습니다.")

        # 주문 정보 출력
        for order in orders:
            print(f"\n🔹 주문 ID: {order.get('orderId')}")
            print(f"   - 생성일: {order.get('creationDate')}")
            print(f"   - 결제 상태: {order.get('orderPaymentStatus')}")
            print(f"   - 배송 상태: {order.get('orderFulfillmentStatus')}")
            print(f"   - 구매자: {order.get('buyer', {}).get('username')}")
            print(f"   - 총 결제 금액: {order.get('pricingSummary', {}).get('total', {}).get('value')} {order.get('pricingSummary', {}).get('total', {}).get('currency')}")
    else:
        print(f"❌ eBay API 호출 실패 (상태 코드: {response.status_code}): {response.text}")
