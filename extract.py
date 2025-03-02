import argparse
import requests
from bs4 import BeautifulSoup

def extract(imageFlag, videoFlag, parsedHTML, webpageURL):
    result = "PATH " + webpageURL + "\n"

    if(imageFlag & videoFlag):
        result+=""
    elif(imageFlag & (not videoFlag)):
        noImagesFilter = parsedHTML.find_all(lambda tag: tag.name not in ["img"])
        noImagesFilter = parsedHTML.find_all("video")
        for tag in noImagesFilter:
            result+="VIDEO: " + str(tag.get("src"))+ " " + str(tag.get("alt")) +"\n"
    elif((not imageFlag) & videoFlag):
        noVideosFilter = parsedHTML.find_all(lambda tag: tag.name not in ["video"])
        noVideosFilter = parsedHTML.find_all("img")
        for tag in noVideosFilter:
            result+="IMAGE: " + str(tag.get("src"))+ " " + str(tag.get("alt")) +"\n"
    else:
        for tag in parsedHTML.find_all(["img", "video"]):
            elementName = ""
            if(tag.name =="img"):
                elementName = "IMAGE "
            elif(tag.name == "video"):
                elementName = "VIDEO "
            result+=elementName + str(tag.get("src"))+ " " + str(tag.get("alt")) +"\n"

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

extract(args.image, args.video, soup, url)