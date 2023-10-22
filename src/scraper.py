import cloudscraper
from bs4 import BeautifulSoup as bs

from utilities import *
from error_handler import *

@base_error_handler
class Scraper():

    @base_error_handler #only handle cloudscraper errors
    def __init__(self,sb,website,out_folder) -> None:
        self.website = website
        self.driver = sb.driver
        self.folder = out_folder
        self.cs_scraper = cloudscraper.create_scraper()
        self.sb = sb

    
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
                        raise InvalidStatusCode(f"{url} returned status code {req.status_code}, should be 200 or 301,302,303,304.","error")
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
            chapter_imgs_filenames = self.downloadChapterImages(chapter_imgs_urls,folder_name)
            mergeImagesToPDF(chapter_imgs_filenames,path)
            clearFolder(path)

    @base_error_handler
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
        status_code =  self.sb.get_link_status_code(url)
        if status_code != 200:
            raise InvalidStatusCode(f"{url} returned status code {status_code}, should be 200 or 301,302,303,304.","critical")
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
    