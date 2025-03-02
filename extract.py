import argparse
import requests
from bs4 import BeautifulSoup

def createFolder(folderName, folderPath):
    print("hello")

def saveFiles():
    print("hi")

def extract(imageFlag, videoFlag, path, parsedHTML, webpageURL):
    result = ""

    if(imageFlag & videoFlag):
        result+=""
    elif(imageFlag & (not videoFlag)):
        noImagesFilter = parsedHTML.find_all("video")
        for tag in noImagesFilter:
            result+="VIDEO: " + str(tag.get("src"))+ " " + str(tag.get("alt")) +"\n"
    elif((not imageFlag) & videoFlag):
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
            src = str(tag.get("src")) if tag.get("src") else ""
            alt = "\"" + str(tag.get("alt")) + "\"" if tag.get("alt") else ""
            result+=elementName + src + " " + alt  +"\n"

    if(path):
        pathString= "PATH " + path + "\n"
        createFolder("Saved Resources", path)
        saveFiles()
        result = pathString + result
        print(result)
    else: 
        pathString= "PATH " + webpageURL + "\n"
        result = pathString + result
        print (result)


def main():
    parser = argparse.ArgumentParser(description="Webscraping script used to display/save images and videos from a webpage url provided")

    # Adding the optional arguments of the command
    parser.add_argument("-i", "--image", action="store_true", help="Exclude images from results")
    parser.add_argument("-v", "--video", action="store_true", help="Exclude videos from results")
    parser.add_argument("-p", "--path", help="Save a copy of the resources locally")

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

    extract(args.image, args.video, args.path, soup, url)

if __name__=="__main__":
    main()

