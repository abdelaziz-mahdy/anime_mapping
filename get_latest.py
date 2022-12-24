import requests
from common import *
mappingFile="latest.json"

latest=readJsonFile(mappingFile)
#revert to only last episode
for key,value in latest.items():
    if isinstance(value,str):
        if value.startswith("EP"):
            latest[key]=int(value[indexOfLastCharacterOfSubstring(value,"EP "):value.index("/")])
page = requests.get("https://api.consumet.org/anime/gogoanime/recent-episodes")
# print(page.content)
jsonObject=page.json()
for anime in jsonObject["results"]: 
    latest[anime["id"]]=anime["episodeNumber"] 

writeJsonFileIfDifferent(mappingFile,latest)
