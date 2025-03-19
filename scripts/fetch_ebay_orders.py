import os
import requests
import time

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

# eBay API 엔드포인트 (Production 환경)
EBAY_API_URL = "https://api.ebay.com/ws/api.dll"

# 요청 헤더 설정 (X-EBAY-API-IAF-TOKEN 추가)
headers = {
    "X-EBAY-API-SITEID": "0",
    "X-EBAY-API-CALL-NAME": "GeteBayOfficialTime",
    "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
    "Content-Type": "text/xml",
    "X-EBAY-API-IAF-TOKEN": EBAY_USER_TOKEN  # ✅ 인증 토큰 추가
}

# XML 요청 바디 (GeteBayOfficialTime API 사용)
xml_body = f"""
<?xml version="1.0" encoding="utf-8"?>
<GeteBayOfficialTimeRequest xmlns="urn:ebay:apis:eBLBaseComponents">
  <RequesterCredentials>
    <eBayAuthToken>{EBAY_USER_TOKEN}</eBayAuthToken>
  </RequesterCredentials>
</GeteBayOfficialTimeRequest>
"""

# 자동 재시도 (503 오류 대비)
MAX_RETRIES = 5
RETRY_DELAY = 10  # 초 단위 (10초 후 재시도)

for attempt in range(1, MAX_RETRIES + 1):
    print(f"\n📡 API 요청 시도 {attempt}/{MAX_RETRIES}...")
    
    try:
        response = requests.post(EBAY_API_URL, data=xml_body, headers=headers)
    except Exception as e:
        print(f"❌ [오류] API 요청 중 예외 발생: {e}")
        exit(1)

    # 응답 상태 코드 확인
    print(f"🔍 응답 코드: {response.status_code}")

    if response.status_code == 200:
        print("✅ API 연결 성공!")
        print("📡 eBay API 응답 데이터:")
        print(response.text)
        break  # 성공했으면 루프 종료

    elif response.status_code == 503:
        print("⚠️ eBay 서버가 응답하지 않음 (503). 잠시 후 다시 시도...")
        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY)  # 재시도 전 대기
        else:
            print("❌ 최대 재시도 횟수 초과. 요청 실패.")
            exit(1)

    else:
        print(f"❌ API 요청 실패: {response.status_code}")
        print("📡 eBay API 응답 데이터 (원본 그대로):")
        print(response.text)
        exit(1)  # 503이 아닌 다른 오류면 즉시 종료
