from seleniumbase import SB
from bs4 import BeautifulSoup as bs
from url_handling import stripAndUseHTTPS

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
        readerarea = soup.find("div",{"id":"readerarea"})
        for image in readerarea.findAll("img"):
            try: #lazy loaded images have a data-src attribute instead of a src attribute
                to_add = image["data-src"]
            except KeyError: 
                to_add = image["src"]
            urls.append(stripAndUseHTTPS(to_add))
    return urls
