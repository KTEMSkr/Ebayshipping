import requests
import os

# GitHub Secrets에서 API Key 가져오기
ACCESS_TOKEN = os.getenv("EBAY_USER_TOKEN")

# eBay 주문 API 호출
url = "https://api.ebay.com/sell/fulfillment/v1/order"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("✅ eBay 주문 목록:", response.json())
else:
    print("❌ eBay API 호출 실패:", response.text)
