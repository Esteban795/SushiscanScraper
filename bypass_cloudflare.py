from seleniumbase import SB
from bs4 import BeautifulSoup as bs

urls = []
with SB(uc=True,headless=True) as sb: #use headless=true to not see Chrome open
    sb.driver.get("https://anime-sama.me/blue-lock-chapitre-217/")
    soup = bs(sb.driver.page_source,'html.parser')
    # print(sb.driver.page_source)
    for image in soup.findAll("img"):
        try:
            to_add = image["data-src"]
        except: 
            to_add = image["src"]
        urls.append(to_add)
print(urls)