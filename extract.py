import argparse
import requests
from bs4 import BeautifulSoup

def extract(imageFlag, videoFlag, parsedHTML):
    result = ""

    if(imageFlag):
        noImagesFilter = parsedHTML.find_all(lambda tag: tag.name not in ["img"])
        noImagesFilter = parsedHTML.find_all("video")
        for tag in noImagesFilter:
            result+=str(tag)
    
    else:
        for tag in parsedHTML.find_all(["img", "video"]):
            result+=str(tag)+"\n"

    print(result)


parser = argparse.ArgumentParser(description="Script pour lire les arguments")

# Adding the optional arguments of the command
parser.add_argument("-i", "--image", action="store_true", help="Exclude images")
parser.add_argument("-v", "--video", action="store_true", help="Exclude videos")

# Adding required argument : URL
parser.add_argument("url", help="URL of the webpage")

# Parsing the arguments
args = parser.parse_args()

# defining the url of the webpage
url = args.url

# fetching the webpage
response = requests.get(url)

# Parsing html
soup = BeautifulSoup(response.text, "html.parser")

extract(args.image, args.video, soup)