import os
import requests
import json

# GitHub Actions 환경 변수 사용
EBAY_USER_TOKEN = os.getenv("EBAY_USER_TOKEN")

# eBay Fulfillment API 엔드포인트 (최신 주문 가져오기)
EBAY_API_URL = "https://api.ebay.com/sell/fulfillment/v1/order"

# API 요청 헤더
headers = {
    "Authorization": f"Bearer {EBAY_USER_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 최신 5개 주문 요청 (날짜 필터 제거)
params = {
    "limit": 5,  # 최신 5개만 가져오기
    "sort": "-creationDate"  # 최신 주문부터 정렬
}

# API 요청 실행
response = requests.get(EBAY_API_URL, headers=headers, params=params)

# 응답 처리
if response.status_code == 200:
    orders_data = response.json()  # JSON 변환
    print("✅ 이베이 API 연결 성공!")

    # 보기 좋게 JSON 출력
    print(json.dumps(orders_data, indent=2, ensure_ascii=False))
else:
    print(f"❌ 이베이 API 요청 실패: {response.status_code}")
    print(response.text)
    exit(1)
