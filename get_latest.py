import requests
from common import *
import cloudscraper
from bs4 import BeautifulSoup

class GogoAnimeParser:
    baseUrl = 'https://gogoanimehd.to'
    classPath = 'ANIME.Gogoanime'
    ajaxUrl = 'https://ajax.gogo-load.com/ajax'

    def __init__(self):
        self.client = requests.Session()

    def fetch_recent_episodes(self, page=1, type=1):
        try:
            res = self.client.get(f"{self.ajaxUrl}/page-recent-release.html?page={page}&type={type}")
            print(f"{self.ajaxUrl}/page-recent-release.html?page={page}&type={type}")
            soup = BeautifulSoup(res.text, 'html.parser')

            recent_episodes = []

            for el in soup.select('div.last_episodes.loaddub > ul > li'):
                href_value = el.find('a')['href']
                id_val = href_value.split('/')[1].split('-episode')[0]
                episode_id = href_value.split('/')[1]
                episode_number = int(el.find('p', class_='episode').text.replace('Episode ', ''))
                title = el.find('p', class_='name').find('a')['title']
                image = el.find('div').find('a').find('img')['src']
                url = f"{self.baseUrl}{el.find('a')['href'].strip()}"

                recent_episodes.append({
                    'id': id_val,
                    'episodeId': episode_id,
                    'episodeNumber': episode_number,
                    'title': title,
                    'image': image,
                    'url': url,
                })

            last_li_class = soup.select('div.anime_name_pagination.intro > div > ul > li')[-1]
            has_next_page = 'selected' not in last_li_class

            return {
                'currentPage': page,
                'hasNextPage': has_next_page,
                'results': recent_episodes,
            }
        except Exception as e:
            raise Exception('Something went wrong. Please try again later.') from e


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
    jsonObject=GogoAnimeParser().fetch_recent_episodes(page)
    print(jsonObject)
    for anime in jsonObject["results"]:         
        if anime["id"] in latest and latest[anime["id"]]==anime["episodeNumber"] :
            gotNew=False
        else:
            latest[anime["id"]]=anime["episodeNumber"] 
            
    page+=1

writeJsonFileIfDifferent(mappingFile,latest)
