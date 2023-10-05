from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import os
from PIL import Image
import requests

def main(url):
    """Downloads all the images at 'url' to /test/"""
    soup = bs(urlopen(url),'lxml')
    urls = []
    for image in soup.findAll("img"):
        urls.append(image["src"].strip())
        # print(f"Image: {image['src']}")
        # filename = image["src"].split("/")[-1]
        # outpath = os.path.join(out_folder, filename)
        # try:
        #     with open(outpath, 'wb') as f:
        #         r = requests.get(url)
        #         f.write(r.content)
        # except Exception as e:
        #     print(e)
    print(urls)
    return urls

def download(urls, out_folder="/test/"):
    j = 0
    for i in urls:
        with open(out_folder + str(j) + "." + i[-3:], 'wb') as f:
            r = requests.get(i)
            f.write(r.content)
        j += 1  
def merge():
    images = [Image.open("./test/" + f) for f in os.listdir("./test/")]
    images[0].save( "./test.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])

if __name__ == "__main__":
    url = "https://sushiscan.fr/jujutsu-kaisen-scan-220-vf/"
    out_folder = "./test/"
    urls =  main(url)
    download(urls,out_folder)
    merge()