xml_body = f"""
<?xml version="1.0" encoding="utf-8"?>
<GetUserRequest xmlns="urn:ebay:apis:eBLBaseComponents">
  <RequesterCredentials>
    <eBayAuthToken>{EBAY_USER_TOKEN}</eBayAuthToken>
  </RequesterCredentials>
</GetUserRequest>
"""

headers["X-EBAY-API-CALL-NAME"] = "GetUser"

response = requests.post(EBAY_API_URL, data=xml_body, headers=headers)

print(f"🔍 응답 코드: {response.status_code}")
print(response.text)  # 응답 데이터 확인
