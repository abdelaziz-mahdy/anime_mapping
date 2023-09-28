from common import *
import cloudscraper
from gogo_anime_parser import GogoAnimeParser
scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance

mappingFile="../latest.json"

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
    jsonObject=GogoAnimeParser(scraper).fetch_recent_episodes(page)
    print(jsonObject)
    for anime in jsonObject["results"]:         
        if anime["id"] in latest and latest[anime["id"]]==anime["episodeNumber"] :
            gotNew=False
        else:
            latest[anime["id"]]=anime["episodeNumber"] 
            
    page+=1

writeJsonFileIfDifferent(mappingFile,latest)
