from bs4 import BeautifulSoup as bs
from seleniumbase import SB 

ALLOWED_WEBSITES = ["anime-sama.me","sushiscan.net","sushiscan.fr"]

def checkValidWebsite(website : str) -> bool:
    return website in ALLOWED_WEBSITES

def searchByName(website : str, name : str):
    if not checkValidWebsite(website):
        print("Website not allowed.")
        exit(1)
    with SB(uc=True,headless=True) as sb:
        sb.driver.get("https://{website}/?s={name}".format(website=website,name="+".join(name.split(" ")))) #replace every blank space by a + 
        soup = bs(sb.driver.page_source,'html.parser')
        children_divs = [a.findChildren()[0] for a in soup.find_all("div",{"class" : "bsx"})]
        results_list = [(a["title"],a["href"]) for a in children_divs]
        return results_list

def chooseFromResults(results_list : list[tuple[str,str]]) -> str:
    res = int(input(f"From your input, here are the available results.Select one : {','.join([i[0] for i in results_list])}"))
    return results_list[res - 1][1]

