"""
dumpimages.py
    Downloads all the images on the supplied URL, and saves them to the
    specified output file ("/test/" by default)

Usage:
    python dumpimages.py http://example.com/ [output]
"""
from bs4 import BeautifulSoup as bs
from urllib.request import (
    urlopen, urlparse, urlunparse, urlretrieve)
import os
import sys
import time
import requests
from PIL import Image
def main(url, out_folder="/test/"):
    """Downloads all the images at 'url' to /test/"""
    soup = bs(urlopen(url),'lxml')
    parsed = list(urlparse(url))
    for image in soup.findAll("img"):
        actual_url = image["src"].strip().replace("http","https")
        print(actual_url[-3:])
        if image["src"][-3:] != "png" and image["src"][-3:] != "jpg":
            continue
        print(f"Image:{image['src']}")
        filename = image["src"].split("/")[-1]
        parsed[2] = image["src"]
        outpath = os.path.join(out_folder, filename)
        try:
            with open("./test/test1.png", 'wb') as f:
                r = requests.get(actual_url)
                print(r.status_code)
                f.write(r.content)
        except Exception as e:
            print(e)

def _usage():
    print("usage: python dumpimages.py http://example.com [outpath]")

def merge():
    images = [Image.open("./test/" + f) for f in os.listdir("./test/")]
    images[0].save( "./test.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])

if __name__ == "__main__":
    url = "https://sushiscan.fr/jujutsu-kaisen-scan-100-vf/"
    out_folder = "./test/"
    if not url.lower().startswith("http"):
        out_folder = sys.argv[-1]
        url = sys.argv[-2]
        if not url.lower().startswith("http"):
            _usage()
            sys.exit(-1)
    main(url, out_folder)
    merge()