from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from PIL import Image
import os
from bypass_cloudflare import bypassCF
from force_fullmode import forceFullMode
from url_handling import stripAnduseHTTPS,checkValidFileExt
import cloudscraper


ALLOWED_WEBSITES = ["anime-sama","sushiscan.net","sushiscan.fr"]

def grabImgURLS(url : str) -> list[str]:
    """Finds every image source link from webpage at `url`.
    Args :
        url : link to the scan
    Returns : 
        list of image urls (EVERY IMAGE OF THE PAGE,EVEN THE ONES NOT PART OF THE MANGA)
    """
    soup = bs(urlopen(url),'lxml')
    readerarea = soup.find("div",{"id":"readerarea"})
    urls = []
    for image in readerarea.find_all("img"):
        url = image["src"]
        urls.append(stripAnduseHTTPS(url)) #for some reasons, some urls have a space right before https://, so we just strip it.
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
                    print(f"Error : status code returned by server is {req.status_code}, should be 200.")
                    clearFolder(out_folder)
                    exit(-1)
                f.write(req.content)
                filenames.append(filename)
            
    return filenames

def mergeImagesTopPDF(filenames,folder):
    """Merges images into a single pdf file
    Args :
        filenames : list of filenames of the images to merge (in the right order, because os.listdir's order is unspecified.
        folder : folder where the images are stored
    """
    images = [Image.open(folder + f) for f in filenames]
    temp = []
    for i in range(len(filenames)):
        if images[i].mode == "RGBA":
            images[i].load()
            background = Image.new("RGB", images[i].size, (255, 255, 255))
            background.paste(images[i], mask=images[i].split()[3])
            temp.append(background)
        else:
            temp.append(images[i])
    temp[0].save(folder[:-1] + ".pdf", "PDF" ,resolution=100.0, save_all=True, append_images=temp[1:])

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
            print("Site not supported yet, thanks to a recent update to Cloudflare. Please use sushiscan.fr or anime-sama.")
        else:
            print("INVALID URL : website not supported. Only sushiscan.fr, sushiscan.net and anime-sama are supported.")
        filenames = downloadImages(urls,out_folder)
        mergeImagesTopPDF(filenames,out_folder)
    except Exception as e:
        print(f"Something went wrong : {e}. Aborting process, removing images from the computer.")
        clearFolder(out_folder)
    else:
        print("Everything went okay!")
        clearFolder(out_folder)
        

