import requests

from bs4 import BeautifulSoup
import re
import requests
from bs4 import BeautifulSoup
import re
import time

class GogoAnimeParser:
    # baseUrl = 'https://gogoanimehd.to'
    classPath = 'ANIME.Gogoanime'
    ajaxUrl = 'https://ajax.gogocdn.net/ajax'

    def __init__(self,client):
        if client:
            self.client = client
        else:
            self.client = requests.Session()
        # self.baseUrl=baseUrl


    def fetch_alternate_domains(self):
        url = 'https://gogotaku.info/'
        for _ in range(3):
            try:
                response = requests.get(url, timeout=2)
                soup = BeautifulSoup(response.text, 'html.parser')
                content_section = soup.select_one('#wrapper_bg > section > section.content_left > div > div.page_content > div > p:nth-child(8)')
                
                # Extract all 'a' tags within the content section
                a_tags = content_section.find_all('a')
                
                # Extract href from each 'a' tag
                urls = [tag['href'] for tag in a_tags if 'gogoanime' in tag['href']]
                
                if urls:
                    return urls
                else:
                    raise Exception('Alternate domains not found in the selected content')
            except requests.exceptions.Timeout:
                time.sleep(2)
                print("time out trying again")
                continue
            except requests.exceptions.RequestException as e:
                print(e)
                break
        return []

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
                episode_text = el.find('p', class_='episode').text.replace('Episode ', '')

                if '.' in episode_text:
                    episode_number = float(episode_text)
                else:
                    episode_number = int(episode_text)
                title = el.find('p', class_='name').find('a')['title']
                image = el.find('div').find('a').find('img')['src']
                # url = f"{self.baseUrl}{el.find('a')['href'].strip()}"

                recent_episodes.append({
                    'id': id_val,
                    'episodeId': episode_id,
                    'episodeNumber': episode_number,
                    'title': title,
                    'image': image,
                    # 'url': url,
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
