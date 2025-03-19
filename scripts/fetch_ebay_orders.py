import os
import requests
import xml.etree.ElementTree as ET

# GitHub Actions 환경 변수 사용
EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")  # Consumer Key (App ID)
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")  # Consumer Secret (Cert ID)
EBAY_USER_TOKEN = os.getenv("EBAY_USER_TOKEN")  # eBay User Token (Auth’n’Auth 방식)

# eBay Trading API (GetOrders) 엔드포인트 (XML 요청 방식)
EBAY_API_URL = "https://api.ebay.com/ws/api.dll"

# 요청 헤더 설정
headers = {
    "X-EBAY-API-SITEID": "0",
    "X-EBAY-API-CALL-NAME": "GetOrders",
    "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
    "Content-Type": "text/xml"
}

# 요청 바디 (최신 5개 주문만 가져오기, 날짜 필터 제거)
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

# 응답 처리
if response.status_code == 200:
    print("✅ 이베이 API 연결 성공!")

    # XML 응답 파싱
    root = ET.fromstring(response.text)
    namespace = {"ns": "urn:ebay:apis:eBLBaseComponents"}

    # 응답 상태 확인
    ack = root.find("ns:Ack", namespace).text
    if ack == "Success":
        print("📦 최신 5개 주문:")
        for order in root.findall(".//ns:Order", namespace):
            order_id = order.find("ns:OrderID", namespace).text
            created_time = order.find("ns:CreatedTime", namespace).text
            buyer = order.find("ns:BuyerUserID", namespace).text
            total = order.find("ns:Total/ns:Value", namespace).text
            currency = order.find("ns:Total/ns:Currency", namespace).text

            print(f"🛒 주문 ID: {order_id}, 구매자: {buyer}, 생성일: {created_time}, 총액: {total} {currency}")
    else:
        print("❌ API 요청은 성공했지만, 데이터가 없습니다.")
else:
    print(f"❌ 이베이 API 요청 실패: {response.status_code}")
    print(response.text)
    exit(1)
