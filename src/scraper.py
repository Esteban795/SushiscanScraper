import cloudscraper

from force_fullmode import forceFullPageMode
from utilities import *
from user import *

def downloadChapterImages(urls : list[str], out_folder : str) -> list[str]:
    """A function to download images from a lists of URLs
    Args : 
        urls : list of urls to download
        out_folder : folder to store the images
    Returns :
        list of filenames of the downloaded images
    """
    filenames = []
    scraper = cloudscraper.create_scraper() #necessary to bypass cloudflare,and as fast as requests
    for url in urls:
        filename = generateFilename(url)
        outpath = f"{out_folder}/{filename}"
        if checkValidFileExt(filename): #svg, gif or stuff like that are not supported by PIL, and they are in fact not part of the manga anyway
            with open(outpath, 'wb') as f:
                req = scraper.get(url,allow_redirects=True)
                if req.status_code != 200:
                    raise InvalidStatusCode(f"{url} returned status code {req.status_code}, should be 200 or 301,302,303,304.")
                f.write(req.content)
                filenames.append(filename)
    return filenames

def getAvailableChapters(sb, url : str) -> list[str]:
    """Returns a list of available chapters from the manga's main page url.
    Args :
        url : link to the manga
    Returns :
        list of available chapters
    """
    sb.driver.get(url)
    soup = bs(sb.driver.page_source,'html.parser')
    chapterlist = soup.find_all("div",{"class" : "eph-num"})
    chapters_urls = [a.findChildren()[0]["href"] for a in chapterlist]
    return chapters_urls

def downloadChapters(sb,chapters : list[str],out_folder : str) -> None:
    """
    Downloads every chapter from the list of chapters's urls.
    Args :
        chapters : list of chapters's urls
        out_folder : folder to store the chapters
    """
    for chapter in chapters:
        folder_name = generateFolderName(chapter)
        path = f"{out_folder}{folder_name}"
        mkdir(path)
        chapter_imgs_urls = forceFullPageMode(sb,chapter)
        chapter_imgs_filenames = downloadChapterImages(chapter_imgs_urls,path)
        mergeImagesToPDF(chapter_imgs_filenames,path)
        clearFolder(path)

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