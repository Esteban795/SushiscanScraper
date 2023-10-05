import requests
url = "https://s22.anime-sama.me/s1/scans/One Piece/1032/12.jpg"

r = requests.get(url)
print(r.status_code)

with open("test.png", 'wb') as f:
    f.write(r.content)