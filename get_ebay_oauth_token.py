import os
import requests
import base64

# ✅ GitHub Actions 환경 확인
if not os.getenv("GITHUB_ENV"):
    print("❌ 이 스크립트는 GitHub Actions에서만 실행됩니다.")
    exit(1)

# ✅ 환경 변수 불러오기 (GitHub Actions Secrets에서 가져옴)
EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
EBAY_REFRESH_TOKEN = os.getenv("EBAY_REFRESH_TOKEN")

if not all([EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_REFRESH_TOKEN]):
    print("❌ eBay API 인증 정보가 없습니다. GitHub Secrets 설정을 확인하세요.")
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

response = requests.post(TOKEN_URL, headers=headers, data=data)

if response.status_code == 200:
    new_access_token = response.json().get("access_token")
    print("✅ eBay Access Token 갱신 완료!")

    # ✅ GitHub Actions 환경 변수로 저장
    with open(os.getenv("GITHUB_ENV"), "a") as github_env:
        github_env.write(f"EBAY_USER_TOKEN={new_access_token}\n")

    print("🔹 새로운 토큰이 GitHub Actions 환경 변수로 설정되었습니다.")

else:
    print(f"❌ Access Token 갱신 실패: {response.text}")
    exit(1)
