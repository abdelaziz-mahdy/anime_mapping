import requests
from bs4 import BeautifulSoup
from common import *
mappingFile="latest.json"

latest=readJsonFile(mappingFile)

page = requests.get("https://animixplay.to/")
# print(page.content)
soup = BeautifulSoup(page.content, "html.parser")
for ultag in soup.select('#resultplace > ul > li'):
    link:str=ultag.find("a")["href"]    
    # print(link[indexOfLastCharacterOfSubstring(link,"/v1/"):link.index("/ep")])
    # print(ultag.find("p",class_="infotext").text)
    try:
        latest[link[indexOfLastCharacterOfSubstring(link,"/v1/"):link.index("/ep")]]=ultag.find("p",class_="infotext").text
    except Exception as e:
        print(e)
        print(link)
        

writeJsonFileIfDifferent(mappingFile,latest)
