import requests
import os
from dotenv import load_dotenv

# 🔹 .env 파일 로드
load_dotenv()

# 🔹 eBay API 인증 정보 불러오기
EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
EBAY_REFRESH_TOKEN = os.getenv("EBAY_REFRESH_TOKEN")

if not all([EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_REFRESH_TOKEN]):
    print("❌ eBay API 인증 정보가 없습니다. 환경 변수를 확인하세요.")
    exit(1)

print("✅ eBay API 인증 정보 로드 완료!")

# 🔹 eBay OAuth Access Token 갱신 함수
def refresh_ebay_user_token():
    """eBay Access Token을 새로 갱신하는 함수"""
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

        # ✅ .env 파일에도 토큰 저장 (토큰 유지)
        with open(".env", "a") as env_file:
            env_file.write(f"\nEBAY_USER_TOKEN={new_access_token}")

        return new_access_token
    else:
        print(f"❌ Access Token 갱신 실패: {response.text}")
        return None


# ✅ 갱신된 Access Token 가져오기 또는 기존 토큰 로드
EBAY_USER_TOKEN = os.getenv("EBAY_USER_TOKEN")

if not EBAY_USER_TOKEN:
    print("🔄 eBay Access Token이 없습니다. 새로 갱신합니다.")
    EBAY_USER_TOKEN = refresh_ebay_user_token()
else:
    print("✅ eBay API 토큰 로드 완료!")

# ✅ 토큰이 없으면 종료
if not EBAY_USER_TOKEN:
    print("❌ eBay Access Token을 가져오지 못했습니다.")
    exit(1)

# ✅ 요청 헤더 설정
headers = {
    "Authorization": f"Bearer {EBAY_USER_TOKEN}",
    "Content-Type": "application/json"
}

# 🔹 eBay API 요청 URL (주문 목록 가져오기)
EBAY_API_URL = "https://api.ebay.com/sell/fulfillment/v1/order?limit=50"

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
