from user import User
from seleniumbase import SB

if __name__ == "__main__":
    website = input("Enter the website you want to download from : ")
    out_folder = input("Enter the folder you want to store the manga in : ")
    with SB(uc=True,headless=True) as sb:
        user = User(sb,website,out_folder)
        user.loop()