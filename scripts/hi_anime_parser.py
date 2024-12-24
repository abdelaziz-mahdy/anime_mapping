import requests
from bs4 import BeautifulSoup
import re
import time


class HiAnimeParser:
    def __init__(self, client=None, base_url="https://hianime.to"):
        self.base_url = base_url
        self.client = client if client else requests.Session()

    def fetch_recent_episodes(self, page=1):
        try:
            response = self.client.get(
                f"{self.base_url}/recently-updated?page={page}")
            print(f"Fetching: {self.base_url}/recently-updated?page={page}")
            soup = BeautifulSoup(response.text, "html.parser")

            episodes = []

            # Extract URLs
            urls = [
                tag["href"]
                for tag in soup.select(
                    '[class^="flw-item"] .film-detail h3 a[href]'
                )
            ]

            # Extract Titles
            titles = [
                tag["data-jname"]
                for tag in soup.select(
                    '[class^="flw-item"] .film-detail h3 a[data-jname]'
                )
            ]

            # Extract Images
            images = [
                tag["data-src"]
                for tag in soup.select(
                    '[class^="flw-item"] .film-poster img[data-src]'
                )
            ]

            # Extract Last Episode Info
            last_episodes = [
                tag.get_text(strip=True)
                for tag in soup.select(
                    '[class^="flw-item"] .film-poster .tick.ltr .tick-item.tick-sub'
                )
            ]

            # Check if there is a Next Page
            has_next_page = bool(
                soup.select_one('li.page-item a[title="Next"]')
            )

            # Combine the extracted data
            for i in range(len(urls)):
                episodes.append(
                    {
                        # Assuming ID is part of the URL
                        "id": "/" + urls[i].split("/")[-1],
                        "title": titles[i],
                        "image": images[i],
                        "episodeNumber": int(last_episodes[i]),
                        "url": f"/{urls[i]}",
                    }
                )

            return {
                "currentPage": page,
                "hasNextPage": has_next_page,
                "results": episodes,
            }
        except Exception as e:
            raise Exception("Failed to fetch recent episodes.") from e


# # Example Usage
# parser = HiAnimeParser()
# recent_episodes
