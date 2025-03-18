import requests
import os

# ✅ 환경 변수에서 가져오기
ACCESS_TOKEN = os.getenv("EBAY_USER_TOKEN")


# 🔥 디버깅: ACCESS_TOKEN 확인
if not ACCESS_TOKEN or ACCESS_TOKEN.strip() == "":
    raise ValueError("❌ ERROR: 환경 변수 `EBAY_USER_TOKEN`이 설정되지 않았습니다!")

print(f"✔️ ACCESS_TOKEN (앞 10자리): {ACCESS_TOKEN[:10]}**********")  # 보안상 앞 10자리만 출력

# ✅ eBay 주문 API URL
ORDER_API_URL = "https://api.ebay.com/sell/fulfillment/v1/order"

# ✅ 요청 헤더 설정
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# ✅ API 요청 실행
response = requests.get(ORDER_API_URL, headers=headers)

# ✅ 응답 확인
if response.status_code == 200:
    orders = response.json()
    print("✔️ eBay 주문 목록 가져오기 성공:", orders)
else:
    print("❌ eBay 주문 목록 가져오기 실패:", response.text)
