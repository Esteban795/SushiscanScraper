from seleniumbase import SB
from bs4 import BeautifulSoup as bs

def bypassCF(url : str) -> list[str]:
    """Grabs every image from source link, even if is protected by Cloudflare.
    Args : 
        url : link to the scan
    Returns :
        list of image urls (EVERY IMAGE OF THE PAGE,EVEN THE ONES NOT PART OF THE MANGA)
    """
    urls = []
    with SB(uc=True,headless=True) as sb: #use headless=true to not see Chrome open (on Windows at least)
        sb.driver.get(url)
        soup = bs(sb.driver.page_source,'html.parser')
        # print(sb.driver.page_source)
        for image in soup.findAll("img"):
            try:
                to_add = image["data-src"]
            except: 
                to_add = image["src"]
            urls.append(to_add)
    return urls
