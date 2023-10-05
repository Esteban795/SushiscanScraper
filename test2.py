import requests

url = "https://opfrcdn.xyz/uploads/manga/jujutsu-kaisen/chapters/100/015.png"

r = requests.get(url)
print(r.status_code)

with open("test.png", 'wb') as f:
    f.write(r.content)