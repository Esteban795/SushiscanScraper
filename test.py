import requests
import json
 
url = "https://sushiscan.net/"
api_url = "http://localhost:8191/v1"
headers = {"Content-Type": "application/json"}
 
data = {
    "cmd": "request.get",
    "url": url,
    "maxTimeout": 60000
}
response = requests.post(api_url, headers=headers, json=data)
print(response.content)
response_data = json.loads(response.content)
cookies = response_data["solution"]["cookies"]
cookies = {cookie["name"]: cookie["value"] for cookie in cookies}
user_agent = response_data["solution"]["userAgent"]
response = requests.get('https://sushiscan.net/wp-content/uploads45/JJKChap247-01.png', cookies=cookies, headers={"User-Agent": user_agent})
with open("test.png", "wb") as f:
    f.write(response.content)