import argparse
import requests
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser(description="Script pour lire les arguments")

# Adding the optional arguments of the command

parser.add_argument("url", help="URL of the webpage")

args = parser.parse_args()

# defining the url of the webpage
url = args.url

# fetching the webpage
response = requests.get(url)

# Parsing html
soup = BeautifulSoup(response.text, "html.parser")

for img in soup.find_all("img"):
    print(img)
