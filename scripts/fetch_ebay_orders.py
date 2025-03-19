import os
import requests

# GitHub Actions 환경 변수 사용
EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
EBAY_USER_TOKEN = os.getenv("EBAY_USER_TOKEN")

# eBay Trading API (GetOrders) 엔드포인트 (XML 기반)
EBAY_API_URL = "https://api.ebay.com/ws/api.dll"

# 요청 헤더 설정
headers = {
    "X-EBAY-API-SITEID": "0",
    "X-EBAY-API-CALL-NAME": "GetOrders",
    "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
    "Content-Type": "text/xml"
}

# 요청 바디 (최신 주문 요청)
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

# API 연결 여부 확인
print("✅ API 연결 성공!") if response.status_code == 200 else print(f"❌ API 요청 실패: {response.status_code}")

# 응답 원본 그대로 출력
print("\n📡 eBay API 응답 데이터:")
print(response.text)
