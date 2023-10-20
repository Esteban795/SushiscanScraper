from bs4 import BeautifulSoup as bs
import re
import os

from utilities import checkValidWebsite,RANGE_PATTERN
from error_handler import *
from scraper import Scraper
from utilities import *

class User():
    def __init__(self,sb,website,out_folder) -> None:
        self.folder = out_folder
        self.website = website
        self.scraper = Scraper(sb,website,out_folder)
        sys.excepthook = except_hook
        if not checkValidWebsite(website):
            raise InvalidWebsite(website)
        
    def searchByName(self, name : str) -> list[tuple[str,str]]:
        """Searches for a manga by its name on the website.
        Args :
            website : website to search on
            name : name of the manga
            
        Returns :
            list of tuples (manga name, manga url)"""
        self.scraper.driver.get(f"https://{self.website}/?s={'+'.join(name.split(' '))}") #replace every blank space by a + 
        soup = bs(self.scraper.driver.page_source,'html.parser')
        children_divs = [a.findChildren()[0] for a in soup.find_all("div",{"class" : "bsx"})]
        results_list = [(a["title"],a["href"]) for a in children_divs]
        return results_list

    def chooseFromResults(self,results_list : list[tuple[str,str]]) -> str:
        """Asks the user to choose a manga from the results list.
        Args :
            results_list : list of tuples (manga name, manga url), generated by searchByName
        Returns :
            url of the chosen manga
        """
        res = int(input(f"From your input, here are the available results.Select one : {', '.join([i[0] for i in results_list])}\n"))
        return results_list[res - 1][1]

    def modifyChaptersList(self,chapters_list : list[str]):
        """Asks the user to choose which chapters to download.
        Args :
            chapters_list : list of chapters's urls
        Returns :
            list of chapters's urls
        """
        res = input(f"There are {len(chapters_list)} chapters available. :\n")
        if res == "all":
            return chapters_list
        elif re.match(RANGE_PATTERN,res):
            start,end = re.findall(RANGE_PATTERN,res)[0]
            if start == "" and end == "":
                raise InvalidRangeFormat(":")
            if start == "":
                start = 1
            if end == "":
                end = len(chapters_list)
            return chapters_list[int(start) - 1:int(end)]
        else:
            raise EmptyResults([])
    
    def loop(self) -> None:
        """Main loop of the program."""
        while True:
            name = input("Enter the name of the manga you want to download : ")
            if name.startswith("http"):
                folder_name = generateFolderName(name)
                folder_path = f"{self.folder}{folder_name}"
                os.mkdir(folder_path)
                images_urls = self.scraper.forceFullPageMode(name)
                images_filenames = self.scraper.downloadChapterImages(images_urls,folder_name)
                mergeImagesToPDF(images_filenames,folder_path)
                clearFolder(folder_path)
            results_list = self.searchByName(name)
            if len(results_list) == 0:
                raise NoResultsFound(name)
            manga_url = self.chooseFromResults(results_list)
            chapters_urls = self.scraper.getAvailableChapters(manga_url)
            chapters_urls = self.modifyChaptersList(chapters_urls)
            self.scraper.downloadChapters(chapters_urls)
    
    def changeWebsite(self) -> None:
        """Changes the website to download from.
        Args :
            new_website : website to download from
        """
        new_website = input(f"Enter the website you want to download from. The ones allowed are : {','.join(ALLOWED_WEBSITES)}")
        if not checkValidWebsite(new_website):
            raise InvalidWebsite(new_website)
        self.website = new_website
        self.scraper.website = new_website