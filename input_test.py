import os
import requests

# ✅ 환경 변수에서 OAuth Access Token 가져오기
ACCESS_TOKEN = os.getenv("EBAY_USER_TOKEN")

if not ACCESS_TOKEN:
    raise ValueError("❌ ERROR: eBay API 토큰이 없습니다! 먼저 토큰을 갱신하세요.")

# ✅ eBay 주문 API URL
EBAY_API_URL = "https://api.ebay.com/sell/fulfillment/v1/order"

# ✅ 요청 헤더 설정
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# ✅ API 요청 실행
response = requests.get(EBAY_API_URL, headers=headers)

# ✅ 응답 확인
if response.status_code == 200:
    orders = response.json().get("orders", [])
    print(f"✔️ {len(orders)}개의 주문을 가져왔습니다.")

    # ✅ 주문 정보 출력
    for order in orders:
        print(f"\n🔹 주문 ID: {order.get('orderId')}")
        print(f"   - 생성일: {order.get('creationDate')}")
        print(f"   - 결제 상태: {order.get('orderPaymentStatus')}")
        print(f"   - 배송 상태: {order.get('orderFulfillmentStatus')}")
        print(f"   - 구매자: {order.get('buyer', {}).get('username')}")
        print(f"   - 총 결제 금액: {order.get('pricingSummary', {}).get('total', {}).get('value')} {order.get('pricingSummary', {}).get('total', {}).get('currency')}")
else:
    print(f"❌ eBay API 호출 실패 (상태 코드: {response.status_code}): {response.text}")
    exit(1)
