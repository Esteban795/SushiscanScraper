from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import os
from PIL import Image
import requests
import re

check_name = re.compile(r"^(?:\d|_)*\.(?:jpg|png)$")
def main(url):
    """Downloads all the images at 'url' to /test/"""
    soup = bs(urlopen(url),'lxml')
    urls = []
    for image in soup.findAll("img"):
        urls.append(image["src"].strip())
    return urls

def download(urls, out_folder="/test/"):
    print(urls)
    for i in urls:
        filename = i.split("/")[-1]
        print(filename)
        res_regex = check_name.findall(filename)
        print(res_regex)
        if res_regex == [] or res_regex[0][0] == '' or res_regex[0][1] == '':
            continue
        outpath = os.path.join(out_folder, filename)
        with open(outpath, 'wb') as f:
            r = requests.get(i)
            print(r.status_code)
            f.write(r.content)

def merge():
    pass
    # images = [Image.open("./test/" + f) for f in os.listdir("./test/")]
    # images[0].save( "./test.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])

if __name__ == "__main__":
    url = "https://sushiscan.fr/dragon-ball-super-scan-79-vf/"
    url_splitted = url.split("/")
    out_folder = "./" + url_splitted[3] + "/"
    os.mkdir(out_folder)
    urls =  main(url)
    download(urls,out_folder)
    merge()
    if len(os.listdir(out_folder)) == 0:
        os.rmdir(out_folder)