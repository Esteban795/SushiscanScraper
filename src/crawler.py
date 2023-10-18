from bs4 import BeautifulSoup as bs
from error_handler import *

ALLOWED_WEBSITES = ["anime-sama.me","sushiscan.net","sushiscan.fr"]

def checkValidWebsite(website : str) -> bool:
    return website in ALLOWED_WEBSITES

def searchByName(sb, website : str, name : str) -> list[tuple[str,str]]:
    if not checkValidWebsite(website):
        raise InvalidWebsite(f"{website} not supported.")
    sb.driver.get("https://{website}/?s={name}".format(website=website,name="+".join(name.split(" ")))) #replace every blank space by a + 
    soup = bs(sb.driver.page_source,'html.parser')
    children_divs = [a.findChildren()[0] for a in soup.find_all("div",{"class" : "bsx"})]
    results_list = [(a["title"],a["href"]) for a in children_divs]
    return results_list

def chooseFromResults(results_list : list[tuple[str,str]]) -> str:
    res = int(input(f"From your input, here are the available results.Select one : {','.join([i[0] for i in results_list])}"))
    return results_list[res - 1][1]

def getAvailableChapters(sb, url : str) -> list[str]:
    """Returns a list of available chapters from the manga's main page url.
    Args :
        url : link to the manga
    Returns :
        list of available chapters
    """
    sb.driver.get(url)
    soup = bs(sb.driver.page_source,'html.parser')
    chapterlist = soup.find_all("div",{"class" :"eph-num"})
    chapters_urls = [a.findChildren()[0]["href"] for a in chapterlist]
    return chapters_urls

if __name__ == "__main__":
    pass