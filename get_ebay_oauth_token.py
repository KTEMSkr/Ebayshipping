import os
import requests
import base64

# ✅ 환경 변수 불러오기
EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
EBAY_REFRESH_TOKEN = os.getenv("EBAY_REFRESH_TOKEN")

print("🔍 디버깅: 환경 변수 확인")
print(f"🔍 EBAY_CLIENT_ID: {'✅ 설정됨' if EBAY_CLIENT_ID else '❌ 없음'}")
print(f"🔍 EBAY_CLIENT_SECRET: {'✅ 설정됨' if EBAY_CLIENT_SECRET else '❌ 없음'}")
print(f"🔍 EBAY_REFRESH_TOKEN: {'✅ 설정됨' if EBAY_REFRESH_TOKEN else '❌ 없음'}")

if not all([EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_REFRESH_TOKEN]):
    print("❌ eBay API 인증 정보가 없습니다. 환경 변수를 확인하세요.")
    exit(1)

# ✅ Basic Auth를 Base64로 직접 인코딩
auth_string = f"{EBAY_CLIENT_ID}:{EBAY_CLIENT_SECRET}"
auth_encoded = base64.b64encode(auth_string.encode()).decode()

TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {auth_encoded}"
}

data = {
    "grant_type": "refresh_token",
    "refresh_token": EBAY_REFRESH_TOKEN,
    "scope": "https://api.ebay.com/oauth/api_scope"
}

print("🔄 eBay Access Token 요청 중...")

response = requests.post(TOKEN_URL, headers=headers, data=data)

# 📌 응답 디버깅 추가
print(f"🔍 응답 상태 코드: {response.status_code}")
print(f"📌 응답 헤더: {response.headers}")
print(f"📌 응답 내용: {response.text}")

if response.status_code == 200:
    new_access_token = response.json().get("access_token")
    print("✅ eBay Access Token 갱신 완료!")

    # ✅ GitHub Actions 환경에서는 `.env` 저장 대신 `GITHUB_ENV`에 저장
    if os.getenv("GITHUB_ENV"):
        with open(os.getenv("GITHUB_ENV"), "a") as github_env:
            github_env.write(f"EBAY_USER_TOKEN={new_access_token}\n")
        print("🔹 새로운 토큰이 GitHub Actions 환경 변수로 설정되었습니다.")
    else:
        print("🔹 로컬 환경: 새로운 토큰을 출력합니다.")
        print(new_access_token)
else:
    print(f"❌ Access Token 갱신 실패: {response.status_code}")
    exit(1)
