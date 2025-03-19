import os
import requests

# GitHub Actions 환경 변수 확인
print("🔍 환경 변수 체크:")
EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
EBAY_USER_TOKEN = os.getenv("EBAY_USER_TOKEN")

if not EBAY_CLIENT_ID or not EBAY_CLIENT_SECRET or not EBAY_USER_TOKEN:
    print("❌ [오류] 환경 변수가 제대로 설정되지 않았습니다!")
    print(f"EBAY_CLIENT_ID: {'✅ 있음' if EBAY_CLIENT_ID else '❌ 없음'}")
    print(f"EBAY_CLIENT_SECRET: {'✅ 있음' if EBAY_CLIENT_SECRET else '❌ 없음'}")
    print(f"EBAY_USER_TOKEN: {'✅ 있음' if EBAY_USER_TOKEN else '❌ 없음'}")
    exit(1)

print("✅ 환경 변수 정상 로드됨.")

# eBay API 엔드포인트 (시간 확인용 API)
EBAY_API_URL = "https://api.ebay.com/ws/api.dll"

# 요청 헤더 설정
headers = {
    "X-EBAY-API-SITEID": "0",
    "X-EBAY-API-CALL-NAME": "GeteBayOfficialTime",
    "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
    "Content-Type": "text/xml"
}

# XML 요청 바디 (가장 간단한 API 요청)
xml_body = f"""
<?xml version="1.0" encoding="utf-8"?>
<GeteBayOfficialTimeRequest xmlns="urn:ebay:apis:eBLBaseComponents">
  <RequesterCredentials>
    <eBayAuthToken>{EBAY_USER_TOKEN}</eBayAuthToken>
  </RequesterCredentials>
</GeteBayOfficialTimeRequest>
"""

# API 요청 실행
print("\n📡 API 요청 시작...")
try:
    response = requests.post(EBAY_API_URL, data=xml_body, headers=headers)
except Exception as e:
    print(f"❌ [오류] API 요청 중 예외 발생: {e}")
    exit(1)

# 응답 상태 코드 확인
print(f"🔍 응답 코드: {response.status_code}")

# 성공 여부 확인
if response.status_code == 200:
    print("✅ API 연결 성공!")
    print("📡 eBay API 응답 데이터:")
    print(response.text)
else:
    print(f"❌ API 요청 실패: {response.status_code}")
    print("📡 eBay API 응답 데이터 (원본 그대로):")
    print(response.text)
