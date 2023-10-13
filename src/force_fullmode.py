from seleniumbase import SB
from bs4 import BeautifulSoup as bs
import os
import time

JS_FUNC = """
elt = document.getElementById("readingmode");
elt.children[0].selected = "selected";
elt.children[1].selected = "";
elt.dispatchEvent(new Event ("change",{"bubbles" : true}));
"""

def forceFullMode(url : str) -> None:
    urls = []
    with SB(uc=True,headless=True) as sb:
        sb.driver.get(url)
        sb.driver.execute_script(JS_FUNC)
        soup = bs(sb.driver.page_source,'html.parser')
        for i in soup.findAll("img"):
            try:
                to_add = i["data-src"]
            except: 
                to_add = i["src"]
            urls.append(to_add)
    return urls


