import requests
import os

# ✅ GitHub Actions에서 환경 변수 가져오기
ACCESS_TOKEN = os.getenv("EBAY_USER_TOKEN")
ORDER_API_URL = "https://api.ebay.com/sell/fulfillment/v1/order"  # eBay 주문 API 엔드포인트

# 🔥 디버깅: `ACCESS_TOKEN` 값이 정상적으로 불러와졌는지 확인
if not ACCESS_TOKEN or ACCESS_TOKEN.strip() == "":
    raise ValueError("❌ ERROR: 환경 변수 `EBAY_USER_TOKEN`이 설정되지 않았습니다!")

if not ACCESS_TOKEN.startswith("v^1.1"):
    raise ValueError("❌ ERROR: ACCESS_TOKEN 값이 올바르지 않습니다! 다시 확인하세요.")

print(f"✔️ ACCESS_TOKEN (앞 10자리): {ACCESS_TOKEN[:10]}**********")  # 보안상 앞 10자리만 출력

# ✅ `Authorization` 헤더 설정
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}".strip(),  # 🔥 `strip()` 추가 (공백 방지)
    "Content-Type": "application/json"
}

# 🔥 디버깅: Authorization 값 확인
if " " in ACCESS_TOKEN:
    raise ValueError(f"❌ ERROR: `ACCESS_TOKEN` 값에 공백이 포함됨! (길이: {len(ACCESS_TOKEN)})")

# ✅ eBay 주문 목록 요청
response = requests.get(ORDER_API_URL, headers=headers)

# 🔍 API 응답 처리
if response.status_code == 200:
    print("✅ eBay 주문 목록:", response.json())  # JSON 응답 출력
else:
    print(f"❌ eBay API 호출 실패: {response.status_code}")
    print(response.json())  # 오류 메시지 출력
