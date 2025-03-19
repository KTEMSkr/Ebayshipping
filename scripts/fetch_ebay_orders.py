import os
import requests
import json
from requests_oauthlib import OAuth1

# GitHub Actions 환경 변수 사용
EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")  # Consumer Key (App ID)
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")  # Consumer Secret (Cert ID)
EBAY_USER_TOKEN = os.getenv("EBAY_USER_TOKEN")  # eBay User Token (Auth’n’Auth 방식)

# eBay Fulfillment API 엔드포인트 (최신 주문 가져오기)
EBAY_API_URL = "https://api.ebay.com/sell/fulfillment/v1/order"

# OAuth1 인증 설정 (Auth’n’Auth 방식 - Token Secret 없음)
auth = OAuth1(
    client_key=EBAY_CLIENT_ID,
    client_secret=EBAY_CLIENT_SECRET,
    resource_owner_key=EBAY_USER_TOKEN
)

# API 요청 헤더 (JSON 응답을 받도록 설정)
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 최신 5개 주문 요청 (날짜 필터 없이 가져오기)
params = {
    "limit": 5,  # 최신 5개만 가져오기
    "sort": "-creationDate"  # 최신 주문부터 정렬
}

# API 요청 실행
response = requests.get(EBAY_API_URL, headers=headers, params=params, auth=auth)

# 응답 처리
if response.status_code == 200:
    try:
        orders_data = response.json()  # JSON 변환
        print("✅ 이베이 API 연결 성공!")
        print(json.dumps(orders_data, indent=2, ensure_ascii=False))  # JSON 보기 좋게 출력
    except json.JSONDecodeError:
        print("❌ 응답을 JSON으로 변환할 수 없습니다. 원본 응답:")
        print(response.text)
else:
    print(f"❌ 이베이 API 요청 실패: {response.status_code}")
    print(response.text)
    exit(1)
