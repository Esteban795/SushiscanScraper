from seleniumbase import SB
from bs4 import BeautifulSoup as bs


urls = []
with SB(uc=True) as sb:
    sb.driver.get("https://sushiscan.net/one-piece-volume-75/")
    soup = bs(sb.driver.page_source,'lxml')
    ele = sb.driver.find_element("#readingmode")
    print(ele)
    sb.driver.execute_script("arguments[0].setAttribute('value', 'full')", ele)
    sb.sleep(2)
    #sb.driver.execute_script(f"document.getElementById('readingmode').setAttribute('value','full')")
    #sb.driver.execute_script("alert(document.getElementByValue('readingmode'))")
    for image in soup.find("img"):
        urls.append(image["src"])
print(urls)

