import os
import requests

# ✅ 환경 변수 불러오기 (GitHub Actions에서 가져옴)
EBAY_USER_TOKEN = os.getenv("EBAY_USER_TOKEN")

if not EBAY_USER_TOKEN:
    print("❌ eBay API 인증 정보가 없습니다. 환경 변수를 확인하세요.")
    exit(1)

# ✅ eBay API 요청 URL (주문 목록 가져오기)
EBAY_API_URL = "https://api.ebay.com/sell/fulfillment/v1/order?limit=50"

headers = {
    "Authorization": f"Bearer {EBAY_USER_TOKEN}",
    "Content-Type": "application/json"
}

# ✅ eBay API 호출
response = requests.get(EBAY_API_URL, headers=headers)

# ✅ Access Token 만료 시 다시 갱신 후 재시도
if response.status_code == 401:  # 🔄 Access Token이 만료된 경우
    print("⚠️ Access Token이 만료되었습니다. 새로 갱신 중...")
    os.system("python get_ebay_oauth_token.py")  # ✅ 새 토큰 갱신

    # ✅ 다시 Access Token 불러오기
    EBAY_USER_TOKEN = os.getenv("EBAY_USER_TOKEN")

    # ✅ 헤더 업데이트
    headers["Authorization"] = f"Bearer {EBAY_USER_TOKEN}"

    # ✅ 다시 요청
    response = requests.get(EBAY_API_URL, headers=headers)

# ✅ 최종 요청 처리
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
