from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from PIL import Image
import os
import requests
import re

checkForValidFilename = re.compile(r"^(?:\d|_)*\.(?:jpg|png)$") #detects patterns like 1.jpg, 1.png, 20_012_120.jpg etc

def grabImgURLS(url : str) -> list[str]:
    """Finds every image source link from webpage at `url`."""
    soup = bs(urlopen(url),'lxml')
    urls = []
    for image in soup.findAll("img"):
        urls.append(image["src"].strip()) #for some reasons, some urls have a space right before https://, so we just strip it.
    return urls

def downloadImages(urls : list[str], out_folder : str) -> list[str]:
    filenames = []
    for url in urls:
        filename = url.split("/")[-1]
        if not re.match(checkForValidFilename,filename): #image isn't of the type used by sushiscan, so it can't be part of the actual manga
            continue
        outpath = os.path.join(out_folder, filename)
        with open(outpath, 'wb') as f:
            r = requests.get(url)
            if r.status_code != 200:
                print(f"Error : status code returned by server is {r.status_code}, should be 200.")
                clearFolder(out_folder)
                exit(-1)
            f.write(r.content)
            filenames.append(filename)
    return filenames

def mergeImagesTopPDF(filenames,folder):
    images = [Image.open(folder + f) for f in filenames]
    images[0].save(folder[:-1] + ".pdf", "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])

def clearFolder(folder):
    for file in os.listdir(folder):
        os.remove(folder + file)
    os.rmdir(folder)

if __name__ == "__main__":
    url = input("Paste the URL of the scan here : ")
    out = input("Specify an absolute (or relative) path to store the manga scan (nothing specified means it will download it in the same folder as SushiscanScraper) : ")
    sep = "./" if out == "" else "/"
    url_splitted = url.split("/")
    out_folder = sep + url_splitted[3] + "/"
    os.mkdir(out_folder) #temp dir to store images until I merge them into a single pdf
    try:
        urls = grabImgURLS(url)
        filenames = downloadImages(urls,out_folder)
        mergeImagesTopPDF(filenames,out_folder)
    except Exception as e:
        print(f"Something went wrong : {e}.Aborting process, removing images from the computer.")
        clearFolder(out_folder)
    else:
        print("Everything went okay!")
        clearFolder(out_folder)

