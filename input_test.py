import requests
import base64
import time

# ✅ eBay API Credentials (개인 환경에 맞게 수정)
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"

# ✅ eBay Token 요청 URL
TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

# ✅ 전역 변수 (초기화)
ACCESS_TOKEN = None
TOKEN_EXPIRY = 0  # 토큰 만료 시간 저장 (초 단위)

def fetch_new_token():
    """새로운 eBay Access Token을 요청하는 함수"""
    global ACCESS_TOKEN, TOKEN_EXPIRY

    # ✅ Base64 인코딩 (client_id:client_secret)
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    # ✅ 요청 헤더
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth_header}"
    }

    # ✅ 요청 데이터
    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    # ✅ eBay Access Token 요청
    response = requests.post(TOKEN_URL, headers=headers, data=data)

    # ✅ 응답 확인
    if response.status_code == 200:
        json_response = response.json()
        ACCESS_TOKEN = json_response["access_token"]
        TOKEN_EXPIRY = time.time() + json_response["expires_in"] - 60  # 60초 여유 두고 만료 설정
        print("✅ 새로운 Access Token 발급 완료!")
        return ACCESS_TOKEN
    else:
        print("❌ Access Token 요청 실패:", response.text)
        return None

def get_access_token():
    """API 호출 전 항상 최신 Access Token을 가져오는 함수"""
    global ACCESS_TOKEN, TOKEN_EXPIRY

    if ACCESS_TOKEN is None or time.time() > TOKEN_EXPIRY:
        print("🔄 Access Token이 만료됨. 새로 발급 중...")
        return fetch_new_token()
    
    return ACCESS_TOKEN

# ✅ eBay API 호출 예제 (토큰 자동 갱신 적용)
def fetch_ebay_orders():
    """eBay 주문 정보를 가져오는 함수"""
    url = "https://api.ebay.com/sell/fulfillment/v1/order?limit=50"

    headers = {
        "Authorization": f"Bearer {get_access_token()}",  # 🔄 항상 최신 토큰 사용
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("✅ eBay API 호출 성공")
        return response.json()
    else:
        print(f"❌ eBay API 호출 실패 (상태 코드: {response.status_code}):", response.text)
        return None

# ✅ 실행 예제
fetch_ebay_orders()
