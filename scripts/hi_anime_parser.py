import requests
from bs4 import BeautifulSoup


class HiAnimeParser:
    def __init__(self, client=None, base_url="https://hianime.to"):
        self.base_url = base_url
        self.client = client if client else requests.Session()

    def fetch_recent_episodes(self, page=1):
        try:
            response = self.client.get(f"{self.base_url}/recently-updated?page={page}")
            print(f"Fetching: {self.base_url}/recently-updated?page={page}")
            soup = BeautifulSoup(response.text, "html.parser")

            episodes = []
            # Find all episode containers
            items = soup.select('[class^="flw-item"]')

            for item in items:
                episode_data = {}

                # Link tag
                link_tag = item.select_one('.film-detail h3 a[href]')
                if link_tag:
                    url_path = link_tag.get("href", "").strip()
                    episode_data["id"] = f"/{url_path.split('/')[-1]}" if url_path else None
                    # If you want to expose the full relative URL
                    episode_data["url"] = f"/{url_path}" if url_path else None

                # Title
                title_tag = item.select_one('.film-detail h3 a[data-jname]')
                if title_tag:
                    episode_data["title"] = title_tag.get("data-jname", "").strip()

                # Image
                img_tag = item.select_one('.film-poster img[data-src]')
                if img_tag:
                    episode_data["image"] = img_tag.get("data-src", "").strip()

                # Episode Number
                last_ep_tag = item.select_one('.film-poster .tick.ltr .tick-item.tick-sub')
                if last_ep_tag:
                    # Attempt to parse as integer
                    try:
                        episode_data["episodeNumber"] = int(last_ep_tag.get_text(strip=True))
                    except ValueError:
                        # If it doesn't parse as integer, you can store as string or skip
                        episode_data["episodeNumber"] = last_ep_tag.get_text(strip=True)
                else:
                    episode_data["episodeNumber"] = 1
                # Only add to list if there's at least one valid field
                if episode_data:
                    episodes.append(episode_data)

            # Check if there is a Next Page
            has_next_page = bool(soup.select_one('li.page-item a[title="Next"]'))

            return {
                "currentPage": page,
                "hasNextPage": has_next_page,
                "results": episodes,
            }

        except Exception as e:
            raise Exception("Failed to fetch recent episodes.") from e


# # Example Usage
# parser = HiAnimeParser()
# recent_episodes = parser.fetch_recent_episodes(1)
# print(recent_episodes)
