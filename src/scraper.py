import cloudscraper
from bs4 import BeautifulSoup as bs

from utilities import *
from error_handler import *

class Scraper():
    def __init__(self,sb,website,out_folder) -> None:
        self.website = website
        self.driver = sb.driver
        self.folder = out_folder
        self.cs_scraper = cloudscraper.create_scraper()

    def downloadChapterImages(self,urls : list[str],folder : str) -> list[str]:
        """A function to download images from a lists of URLs
        Args : 
            urls : list of urls to download
            out_folder : folder to store the images
        Returns :
            list of filenames of the downloaded images
        """
        filenames = []
        for url in urls:
            filename = generateFilename(url)
            outpath = f"{self.folder}{folder}{filename}"
            if checkValidFileExt(filename): #svg, gif or stuff like that are not supported by PIL, and they are in fact not part of the manga anyway
                with open(outpath, 'wb') as f:
                    req = self.cs_scraper.get(url,allow_redirects=True)
                    if req.status_code != 200:
                        raise InvalidStatusCode(f"{url} returned status code {req.status_code}, should be 200 or 301,302,303,304.")
                    f.write(req.content)
                    filenames.append(filename)
        return filenames
    
    def getAvailableChapters(self, url : str) -> list[str]:
        """Returns a list of available chapters from the manga's main page url.
        Args :
            url : link to the manga
        Returns :
            list of available chapters
        """
        self.driver.get(url)
        soup = bs(self.driver.page_source,'html.parser')
        chapterlist = soup.find_all("div",{"class" : "eph-num"})
        chapters_urls = [a.findChildren()[0]["href"] for a in chapterlist]
        return chapters_urls

    def downloadChapters(self,chapters : list[str]) -> None:
        """
        Downloads every chapter from the list of chapters's urls.
        Args :
            chapters : list of chapters's urls
            out_folder : folder to store the chapters
        """
        for chapter in chapters:
            folder_name = generateFolderName(chapter)
            path = f"{self.folder}{folder_name}"
            mkdir(path)
            chapter_imgs_urls = self.forceFullPageMode(chapter)
            chapter_imgs_filenames = self.downloadChapterImages(chapter_imgs_urls)
            mergeImagesToPDF(chapter_imgs_filenames,path)
            clearFolder(path)

    def forceFullPageMode(self,url : str) -> list[str]:
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
        self.driver.get(url)
        self.driver.execute_script(JS_FUNC)
        soup = bs(self.driver.page_source,'html.parser')
        readerarea = soup.find("div",{"id":"readerarea"})
        for img in readerarea.findAll("img"):
            try:
                to_add = img["data-src"]
            except: 
                to_add = img["src"]
            urls.append(stripAndUseHTTPS(to_add))
        return urls
    

# if __name__ == "__main__":
#     url = input("Paste the URL of the scan here : ")
#     out = input("Specify an absolute (or relative) path to store the manga scan (nothing specified means it will download it in the same folder as SushiscanScraper) : ")
#     sep = "./" if out == "" else "/"
#     url_splitted = url.split("/")
#     out_folder = f"{sep}{url_splitted[-2]}/"
#     os.mkdir(out_folder) #temp dir to store images until I merge them into a single pdf
#     try:
#         if "sushiscan.fr" in url: #sushiscan.fr isn't protected by cloudflare, no needs to bypass anything
#             urls = grabImgURLS(url)
#         elif "anime-sama" in url:
#             urls = forceFullMode(url)
#         elif "sushiscan.net" in url:
#             #urls = forceFullMode(url)
#             print("Site not supported yet. Please use sushiscan.fr or anime-sama.me")
#         else:
#             print("INVALID URL : website not supported. Only sushiscan.fr, sushiscan.net and anime-sama are supported.")
#         filenames = downloadImages(urls,out_folder)
#         mergeImagesToPDF(filenames,out_folder)
#     except Exception as e:
#         print(f"Something went wrong : {e}. Aborting process, removing images from the computer.")
#         clearFolder(out_folder)
#     else:
#         print("Everything went okay!")
#         clearFolder(out_folder)