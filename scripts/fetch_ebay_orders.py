import os
import requests

# GitHub Actions 환경 변수 사용
EBAY_USER_TOKEN = os.getenv("EBAY_USER_TOKEN")

# eBay Trading API 엔드포인트 (테스트용)
EBAY_API_URL = "https://api.ebay.com/ws/api.dll"

# 요청 헤더 설정
headers = {
    "X-EBAY-API-SITEID": "0",
    "X-EBAY-API-CALL-NAME": "GeteBayOfficialTime",
    "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
    "Content-Type": "text/xml"
}

# 요청 바디 (GeteBayOfficialTime - 단순한 API 호출)
xml_body = f"""
<?xml version="1.0" encoding="utf-8"?>
<GeteBayOfficialTimeRequest xmlns="urn:ebay:apis:eBLBaseComponents">
  <RequesterCredentials>
    <eBayAuthToken>{EBAY_USER_TOKEN}</eBayAuthToken>
  </RequesterCredentials>
</GeteBayOfficialTimeRequest>
"""

# API 요청 실행
response = requests.post(EBAY_API_URL, data=xml_body, headers=headers)

# API 연결 여부 확인
if response.status_code == 200:
    print("✅ API 연결 성공!")
else:
    print(f"❌ API 요청 실패: {response.status_code}")
    print(response.text)  # 오류 메시지 확인
