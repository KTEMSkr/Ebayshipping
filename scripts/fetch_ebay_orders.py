import os
import requests
from requests_oauthlib import OAuth1

# GitHub Actions 환경 변수 사용
EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")  # Consumer Key (App ID)
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")  # Consumer Secret (Cert ID)
EBAY_USER_TOKEN = os.getenv("EBAY_USER_TOKEN")  # eBay User Token (Auth’n’Auth 방식)

# eBay Trading API (GetOrders) 엔드포인트 (XML 기반)
EBAY_API_URL = "https://api.ebay.com/ws/api.dll"

# 요청 헤더 설정
headers = {
    "X-EBAY-API-SITEID": "0",
    "X-EBAY-API-CALL-NAME": "GetOrders",
    "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
    "Content-Type": "text/xml"
}

# 요청 바디 (최신 5개 주문 가져오기)
xml_body = f"""
<?xml version="1.0" encoding="utf-8"?>
<GetOrdersRequest xmlns="urn:ebay:apis:eBLBaseComponents">
  <RequesterCredentials>
    <eBayAuthToken>{EBAY_USER_TOKEN}</eBayAuthToken>
  </RequesterCredentials>
  <OrderRole>Seller</OrderRole>
  <OrderStatus>Completed</OrderStatus>
  <Pagination>
    <EntriesPerPage>5</EntriesPerPage>
    <PageNumber>1</PageNumber>
  </Pagination>
</GetOrdersRequest>
"""

# API 요청 실행
response = requests.post(EBAY_API_URL, data=xml_body, headers=headers)

# 응답 처리 (원본 데이터 그대로 출력)
print("✅ 이베이 API 연결 성공!") if response.status_code == 200 else print(f"❌ 이베이 API 요청 실패: {response.status_code}")

print("\n📡 eBay API 응답 데이터 (원본 그대로):")
print(response.text)  # XML 원본 그대로 출력
