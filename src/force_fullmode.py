from bs4 import BeautifulSoup as bs
from url_handling import *

def forceFullPageMode(sb,url : str) -> list[str]:
    """
    forces the website to display the manga in full page mode.
    Args :
        url : url of the manga
    Returns :
        list of urls of the images
    """
    urls = []
    JS_FUNC = """
    elt = document.getElementById("readingmode");
    elt.children[0].selected = "selected";
    elt.children[1].selected = "";
    elt.dispatchEvent(new Event ("change",{"bubbles" : true}));
    """
    sb.driver.get(url)
    sb.driver.execute_script(JS_FUNC)
    soup = bs(sb.driver.page_source,'html.parser')
    readerarea = soup.find("div",{"id":"readerarea"})
    for i in readerarea.findAll("img"):
        try:
            to_add = i["data-src"]
        except: 
            to_add = i["src"]
        urls.append(stripAndUseHTTPS(to_add))
    return urls


