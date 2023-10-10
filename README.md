# SushiscanScraper
## A python script to bulk download scans from Sushiscan.


# /!\ WARNING

- It currently only works with the website `sushiscan.fr` (because sushiscan.net is protected by cloudflare, which makes it harder to enter correctly. I'm currently working on a way to bypass it, and provide full accessibility to sushiscan.net full catalogue.)

### Requirements 
- Python 3.10.0 and above should work just fine.
- See `requirements.txt`.
### Installation

- Clone it via git, or download the zip and extract in the desired folder. 

### Usage

- You can then run the program using python, which should propose something like this : 
![scraperexample](./examples/scraper.png)

- If you see any other message than "Everything went okay!", please double check the URL you provided before opening an issue here. The error handler system is not fully working right now.

Enjoy.

### Objectives :

- Bypass cloudflare to allow people to have access to a bigger library. (i.e using sushiscan.net URLs instead of sushiscan.fr)
- Allow to bulk download (like download every single page of a manga at once, or downloading only certain chapters, or downloading a range of chapters)
- Because sushiscan.net already grouped certain span of chapters together into volumes, I'll try adding an option to download a specific volume alone.