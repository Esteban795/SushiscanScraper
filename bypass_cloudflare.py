from seleniumbase import SB
from bs4 import BeautifulSoup as bs


urls = []
with SB(uc=True) as sb: #use headless=true to not see Chrome open
    sb.driver.get("https://anime-sama.me/blue-lock-chapitre-217/")
    soup = bs(sb.driver.page_source,'lxml')
    print(sb.driver.page_source)
    for image in soup.findAll("img"):
        urls.append(image["src"])
#print(urls)