import argparse
import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse

def createFolder(folderPath):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    else:
        print("Directory Already exists")

def saveFiles(resources, folderPath):
    savedFiles = []
    for res in resources:
        img_data = requests.get(res["url"]).content
        parsedURL = urlparse(res["url"])
        fileName = os.path.basename(parsedURL.path)
        filePath = os.path.join(folderPath, fileName)
        savedFiles.append({"type": res["type"], "path":filePath, "alt":res["alt"]})

        with open(filePath, 'wb') as handler:
            handler.write(img_data)
    
    return savedFiles

def extract(imageFlag, videoFlag, path, regex, parsedHTML, webpageURL):
    resources = []

    if(imageFlag and (not videoFlag)):
        noImagesFilter = parsedHTML.find_all("video")
        for tag in noImagesFilter:
            sourceTag = tag.find("source")
            src = sourceTag["src"] if sourceTag and sourceTag.get("src") else ""
            resources.append({"type": "VIDEO", "url": urljoin(webpageURL, src), "alt":""})

    elif((not imageFlag) and videoFlag):
        noVideosFilter = parsedHTML.find_all("img")
        for tag in noVideosFilter:
            src = tag.get("src", "")
            alt = "\"" + str(tag.get("alt")) + "\"" if tag.get("alt") else ""
            resources.append({"type": "IMAGE", "url": urljoin(webpageURL, src), "alt":alt})

    else:
        for tag in parsedHTML.find_all(["img", "video"]):
            resourceType = ""
            if(tag.name =="img"):
                resourceType = "IMAGE"
                src = tag.get("src") if tag.get("src") else ""
                alt = tag.get("alt", "")

            elif(tag.name == "video"):
                resourceType = "VIDEO"
                # Sometimes video elements don't have a src attribute but other elements inside <source>
                sourceTag = tag.find("source")
                src = sourceTag["src"] if sourceTag and sourceTag.get("src") else ""
                alt = ""

            alt = "\"" + str(tag.get("alt")) + "\"" if tag.get("alt") else ""

            resources.append({"type": resourceType, "url": urljoin(webpageURL, src), "alt": alt})

    if (regex):
        resources = [res for res in resources if regex in res['url']]

    if(path):
        pathString= "PATH " + path
        createFolder(path)
        savedFiles = saveFiles(resources, path)
        print(pathString)
        for file in savedFiles:
            print(file['type'] + ": " + file['path'] + " " + file['alt'])
    else: 
        pathString= "PATH " + webpageURL
        print(pathString)
        for res in resources:
            print(res['type'] + ": " + res['url'] + " " + res['alt'])


def main():
    parser = argparse.ArgumentParser(description="Webscraping script used to display/save images and videos from a webpage url provided")

    # Adding the optional arguments of the command
    parser.add_argument("-i", "--image", action="store_true", help="Exclude images from results")
    parser.add_argument("-v", "--video", action="store_true", help="Exclude videos from results")
    parser.add_argument("-p", "--path", help="Save a copy of the resources locally")
    parser.add_argument("-r", "--regex", help="Filter the resources that contain the sequence of characters provided")


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

    extract(args.image, args.video, args.path, args.regex, soup, url)

if __name__=="__main__":
    main()