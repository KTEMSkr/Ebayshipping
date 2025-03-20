import os
import requests
import base64

# ✅ 환경 변수에서 가져오기
CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("EBAY_REFRESH_TOKEN")

# ✅ 필수 환경 변수 확인
if not all([CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN]):
    raise ValueError("❌ ERROR: eBay API 인증 정보가 없습니다! 환경 변수를 확인하세요.")

# ✅ eBay OAuth Token 요청 URL
TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

# ✅ Basic 인증을 위한 Base64 인코딩
credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

# ✅ 요청 헤더 및 바디
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {encoded_credentials}"
}
data = {
    "grant_type": "refresh_token",
    "refresh_token": REFRESH_TOKEN,
    "scope": "https://api.ebay.com/oauth/api_scope/sell.fulfillment"
}

# ✅ API 요청 실행
response = requests.post(TOKEN_URL, headers=headers, data=data)

# ✅ 응답 확인
if response.status_code == 200:
    token_data = response.json()
    ACCESS_TOKEN = token_data["access_token"]
    print("✔️ eBay OAuth 토큰 발급 성공:", ACCESS_TOKEN[:10] + "********")

    # ✅ GitHub Actions 환경 변수에 저장
    if os.getenv("GITHUB_ENV"):
        with open(os.getenv("GITHUB_ENV"), "a") as github_env:
            github_env.write(f"EBAY_USER_TOKEN={ACCESS_TOKEN}\n")
        print("🔹 새로운 토큰이 GitHub Actions 환경 변수로 설정되었습니다.")
    else:
        print("🔹 로컬 환경: 새로운 토큰을 출력합니다.")
        print(ACCESS_TOKEN)

else:
    print(f"❌ Access Token 갱신 실패: {response.status_code}")
    print(f"📌 응답 내용: {response.text}")
    exit(1)
