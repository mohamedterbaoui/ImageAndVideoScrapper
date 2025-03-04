import argparse
import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def createFolder(folderName, folderPath):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    else:
        print("Directory Already exists")

def saveFiles(resources, folderPath):
    filesPaths = []
    for res in resources:
        img_data = requests.get(res["url"]).content
        fileName = res["url"].split('/')[-1]
        filePath = os.path.join(folderPath, fileName)
        filesPaths.append({"type": res["type"], "path":filePath})

        with open(filePath, 'wb') as handler:
            handler.write(img_data)
    
    return filesPaths

def extract(imageFlag, videoFlag, path, parsedHTML, webpageURL):
    result = ""
    resources = []


    if(imageFlag and videoFlag):
        result+=""
    elif(imageFlag and (not videoFlag)):
        noImagesFilter = parsedHTML.find_all("video")
        for tag in noImagesFilter:
            result+="VIDEO: " + str(tag.get("src"))+ " " + str(tag.get("alt")) +"\n"
            resources.append({"type": "VIDEO", "url": urljoin(webpageURL, tag.get("src"))})
    elif((not imageFlag) and videoFlag):
        noVideosFilter = parsedHTML.find_all("img")
        for tag in noVideosFilter:
            result+="IMAGE: " + str(tag.get("src"))+ " " + str(tag.get("alt")) +"\n"
            resources.append({"type": "IMAGE", "url": urljoin(webpageURL, tag.get("src"))})
    else:
        for tag in parsedHTML.find_all(["img", "video"]):
            resourceType = ""
            if(tag.name =="img"):
                resourceType = "IMAGE "
            elif(tag.name == "video"):
                resourceType = "VIDEO "
            src = str(tag.get("src")) if tag.get("src") else ""
            alt = "\"" + str(tag.get("alt")) + "\"" if tag.get("alt") else ""
            result+=resourceType + src + " " + alt  +"\n"
            resources.append({"type": resourceType, "url": urljoin(webpageURL, tag.get("src"))})

    if(path):
        pathString= "PATH " + path + "\n"
        createFolder("Saved Resources", path)
        localPaths = saveFiles(resources, path)
        result = pathString + result
        print(result)
        print(localPaths)
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

