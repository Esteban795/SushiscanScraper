ALLOWED_WEBSITES = ["anime-sama.me","sushiscan.fr","sushiscan.net"]

def stripAndUseHTTPS(url : str) -> str:
    correct_url = url.strip() #some urls have a space before it, don't ask me why
    if correct_url[:4] == "http" and correct_url[4] != "s": #some urls are http:// instead of https which throws 404
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

def checkValidWebsite(website : str) -> bool:
    return website in ALLOWED_WEBSITES
