import requests
import os

# ✅ GitHub Secrets에서 eBay API Access Token 가져오기
ACCESS_TOKEN = os.getenv("EBAY_USER_TOKEN")

if not ACCESS_TOKEN:
    raise ValueError("❌ ERROR: `EBAY_USER_TOKEN`이 설정되지 않았습니다!")

# ✅ eBay 주문 API URL (예제: 주문 목록 조회)
ORDER_API_URL = "https://api.ebay.com/sell/fulfillment/v1/order"

# ✅ 헤더 설정 (공백 방지)
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}".strip(),
    "Content-Type": "application/json"
}

# 🔥 디버깅: Authorization 값 확인
if " " in ACCESS_TOKEN:
    raise ValueError(f"❌ ERROR: `ACCESS_TOKEN` 값에 공백이 포함됨! (길이: {len(ACCESS_TOKEN)})")

# ✅ eBay 주문 조회 요청 보내기
response = requests.get(ORDER_API_URL, headers=headers)

# ✅ 응답 확인
if response.status_code == 200:
    print("✅ eBay 주문 목록 조회 성공:", response.json())
else:
    print(f"❌ eBay API 호출 실패 (상태 코드: {response.status_code}):", response.text)
