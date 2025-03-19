import os
import requests
from requests_oauthlib import OAuth1

# GitHub Actions 환경 변수 사용
EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
EBAY_USER_TOKEN = os.getenv("EBAY_USER_TOKEN")

# API URL 설정
EBAY_API_URL = "https://api.ebay.com/ws/api.dll"

# 요청 헤더 설정
headers = {
    "X-EBAY-API-SITEID": "0",
    "X-EBAY-API-CALL-NAME": "GetOrders",
    "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
    "Content-Type": "text/xml"
}

# 요청 바디 (최근 7일간 주문 조회)
xml_body = f"""
<?xml version="1.0" encoding="utf-8"?>
<GetOrdersRequest xmlns="urn:ebay:apis:eBLBaseComponents">
  <RequesterCredentials>
    <eBayAuthToken>{EBAY_USER_TOKEN}</eBayAuthToken>
  </RequesterCredentials>
  <CreateTimeFrom>2024-03-12T00:00:00Z</CreateTimeFrom>
  <CreateTimeTo>2024-03-19T23:59:59Z</CreateTimeTo>
  <OrderRole>Seller</OrderRole>
  <OrderStatus>Completed</OrderStatus>
</GetOrdersRequest>
"""

# API 요청 실행
response = requests.post(EBAY_API_URL, data=xml_body, headers=headers)

# 응답 처리
if response.status_code == 200:
    print("✅ 이베이 API 연결 성공!")
    print(response.text[:500])  # 일부 데이터만 출력
else:
    print(f"❌ 이베이 API 요청 실패: {response.status_code}")
    print(response.text)
    exit(1)
