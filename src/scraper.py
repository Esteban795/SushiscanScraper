from bs4 import BeautifulSoup as bs
import requests
from PIL import Image
import os
from bypass_cloudflare import bypassCF
from url_handling import stripAndUseHTTPS,checkValidFileExt
import cloudscraper
from error_handler import *

ALLOWED_WEBSITES = ["anime-sama","sushiscan.net","sushiscan.fr"]

def grabImgURLS(url : str) -> list[str]:
    """Finds every image source link from webpage at `url`.
    Args :
        url : link to the scan
    Returns : 
        list of image urls (EVERY IMAGE OF THE PAGE,EVEN THE ONES NOT PART OF THE MANGA)
    """
    soup = bs(requests.get(url).text,'lxml')
    readerarea = soup.find("div",{"id":"readerarea"})
    urls = []
    for image in readerarea.find_all("img"):
        url = image["src"]
        urls.append(stripAndUseHTTPS(url)) #for some reasons, some urls have a space right before https://, so we just strip it.
    return urls

def downloadImages(urls : list[str], out_folder : str) -> list[str]:
    """A function to download images from a lists of URLs
    Args : 
        urls : list of urls to download
        out_folder : folder to store the images
    Returns :
        list of filenames of the downloaded images
    """
    filenames = []
    scraper = cloudscraper.create_scraper()
    for url in urls:
        filename = url.split("/")[-1]
        outpath = os.path.join(out_folder, filename)
        if checkValidFileExt(filename): #svg, gif or stuff like that are not supported by PIL, and they are in fact not part of the manga anyway
            with open(outpath, 'wb') as f:
                req = scraper.get(url,allow_redirects=True)
                if req.status_code != 200:
                    clearFolder(out_folder)
                    raise InvalidStatusCode(f"{url} returned status code {req.status_code}, should be 200 or 301,302,303,304.")
                f.write(req.content)
                req.co
                filenames.append(filename)
    return filenames

def mergeImagesToPDF(filenames,folder):
    """Merges path_images into a single pdf file
    Args :
        filenames : list of filenames of the path_images to merge (in the right order, because os.listdir's order is unspecified.
        folder : folder where the path_images are stored
    """
    path_images = [Image.open(folder + f) for f in filenames]
    images = []
    for i in range(len(filenames)):
        if path_images[i].mode == "RGBA":
            path_images[i].load()
            background = Image.new("RGB", path_images[i].size, (255, 255, 255))
            background.paste(path_images[i], mask=path_images[i].split()[3])
            images.append(background)
        else:
            images.append(path_images[i])
    images[0].save(folder[:-1] + ".pdf", "PDF" ,resolution=100.0, save_all=True, append_path_images=images[1:])

def clearFolder(folder):
    """Removes all files from a folder, then removes the folder itself.
    Args :
        folder : path of the folder to remove.
    """
    for file in os.listdir(folder):
        os.remove(folder + file)
    os.rmdir(folder)

if __name__ == "__main__":
    url = input("Paste the URL of the scan here : ")
    out = input("Specify an absolute (or relative) path to store the manga scan (nothing specified means it will download it in the same folder as SushiscanScraper) : ")
    sep = "./" if out == "" else "/"
    url_splitted = url.split("/")
    out_folder = sep + url_splitted[-2] + "/"
    os.mkdir(out_folder) #temp dir to store images until I merge them into a single pdf
    try:
        if "sushiscan.fr" in url: #sushiscan.fr isn't protected by cloudflare, no needs to bypass anything
            urls = grabImgURLS(url)
        elif "anime-sama" in url:
            urls = bypassCF(url)
        elif "sushiscan.net" in url:
            #urls = forceFullMode(url)
            print("Site not supported yet. Please use sushiscan.fr or anime-sama.me")
        else:
            print("INVALID URL : website not supported. Only sushiscan.fr, sushiscan.net and anime-sama are supported.")
        filenames = downloadImages(urls,out_folder)
        mergeImagesToPDF(filenames,out_folder)
    except Exception as e:
        print(f"Something went wrong : {e}. Aborting process, removing images from the computer.")
        clearFolder(out_folder)
    else:
        print("Everything went okay!")
        clearFolder(out_folder)