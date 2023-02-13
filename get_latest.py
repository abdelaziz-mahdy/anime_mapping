import requests
from common import *
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
    pageData = requests.get(f"https://api.consumet.org/anime/gogoanime/recent-episodes?page={page}",headers={"Content-Type": "application/json","User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"})
    print(pageData.content)
    jsonObject=pageData.json()
    for anime in jsonObject["results"]:         
        if anime["id"] in latest and latest[anime["id"]]==anime["episodeNumber"] :
            gotNew=False
        else:
            latest[anime["id"]]=anime["episodeNumber"] 
            
    page+=1

writeJsonFileIfDifferent(mappingFile,latest)
