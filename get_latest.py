import requests
from common import *
import cloudscraper

scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
mappingFile="latest.json"

latest=readJsonFile(mappingFile)
# #revert to only last episode
# for key,value in latest.items():
#     if isinstance(value,str):
#         if value.startswith("EP"):
#             latest[key]=int(value[indexOfLastCharacterOfSubstring(value,"EP "):value.index("/")])
page=1
gotNew=True
while gotNew:
    print(f"loading page {page}")
    pageData = scraper.get(f"https://api.consumet.org/anime/gogoanime/recent-episodes?page={page}")
    print(pageData.content)
    jsonObject=pageData.json()
    for anime in jsonObject["results"]:         
        if anime["id"] in latest and latest[anime["id"]]==anime["episodeNumber"] :
            gotNew=False
        else:
            latest[anime["id"]]=anime["episodeNumber"] 
            
    page+=1

writeJsonFileIfDifferent(mappingFile,latest)
