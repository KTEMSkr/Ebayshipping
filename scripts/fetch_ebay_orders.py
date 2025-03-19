import os
import requests
import json

# GitHub Actions 환경 변수 사용
EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
EBAY_USER_TOKEN = os.getenv("EBAY_USER_TOKEN")

# API URL 설정
EBAY_API_URL = "https://api.ebay.com/sell/fulfillment/v1/order"

# API 요청 헤더
headers = {
    "Authorization": f"Bearer {EBAY_USER_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 최근 7일 주문 가져오기
params = {
    "filter": "creationDate:[2024-03-12T00:00:00.000Z..2024-03-19T23:59:59.000Z]",
    "limit": 5  # 5개 주문만 가져와 테스트
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
