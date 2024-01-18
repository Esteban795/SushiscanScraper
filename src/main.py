from user import User
from seleniumbase import SB
from utilities import checkValidWebsite,ALLOWED_WEBSITES

import os


if __name__ == "__main__":
    out_folder = input("Enter the folder you want to store the manga in : ")
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
    with SB(uc=True,headless=True) as sb:
        user = User(sb,out_folder)
        user.loop()