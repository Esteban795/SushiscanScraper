from PIL import Image
from os import mkdir,rmdir,listdir,remove
import re

RANGE_PATTERN = re.compile(r"^(\d*)?(?:-|:)(\d*)?$") #detects patterns like 1:5 or 1-5, :5, 5:

def stripAndUseHTTPS(url : str) -> str:
    correct_url = url.strip() #some urls have a space before it, don't ask me why
    if correct_url[:4] == "http" and correct_url[4] != "s": #some urls are http instead of https which throws 404
        correct_url = correct_url.replace("http","https")
    return correct_url

def checkValidFileExt(filename : str) -> bool:
    """Checks if the file extension is supported by PIL.
    Args :
        filename : name of the file to check
    Returns :
        True if the file extension is supported, False otherwise.
    """
    valid_ext = ["jpg","jpeg","png","bmp","webp"]
    return filename[-3:].lower() in valid_ext

def generateFilename(url : str) -> str:
    """Generates a filename from an url
    Args :
        url : url of the image
    Returns :
        filename
    """
    return url.split("/")[-1]

def clearFolder(folder):
    """Removes all files from a folder, then removes the folder itself.
    Args :
        folder : path of the folder to remove.
    """
    for file in listdir(folder):
        remove(f"{folder}{file}")
    rmdir(folder)

def generateFolderName(chapter_url : str) -> str:
    """Generates a folder name from the chapter url
    Args :
        chapter_url : url of the chapter
    Returns :
        folder name
    """
    return f"{chapter_url.split('/')[-2]}/"

def mergeImagesToPDF(filenames : list[str],folder : str) -> None:
    """Merges path_images into a single pdf file
    Args :
        filenames : list of filenames of the path_images to merge (in the right order, because os.listdir's order is unspecified.
        folder : folder where the path_images are stored
    """
    images = [Image.open(f"{folder}{f}") for f in filenames]
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