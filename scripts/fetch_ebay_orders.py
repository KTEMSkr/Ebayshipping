EBAY_API_URL = "https://api.ebay.com/ws/api.dll"

headers = {
    "X-EBAY-API-SITEID": "0",
    "X-EBAY-API-CALL-NAME": "GetMyeBaySelling",
    "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
    "Content-Type": "text/xml"
}

xml_body = f"""
<?xml version="1.0" encoding="utf-8"?>
<GetMyeBaySellingRequest xmlns="urn:ebay:apis:eBLBaseComponents">
  <RequesterCredentials>
    <eBayAuthToken>{EBAY_USER_TOKEN}</eBayAuthToken>
  </RequesterCredentials>
  <ActiveList>
    <Include>true</Include>
  </ActiveList>
</GetMyeBaySellingRequest>
"""

response = requests.post(EBAY_API_URL, data=xml_body, headers=headers)

if response.status_code == 200:
    print("✅ eBay API 연결 성공!")
    print(response.text[:500])  # 일부 데이터 출력
else:
    print(f"❌ 이베이 API 요청 실패: {response.status_code}")
    print(response.text)
    exit(1)
