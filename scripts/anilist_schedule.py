import requests
import time

class AnilistSchedule:
    def __init__(self,client):
        self.base_url = "https://graphql.anilist.co"
        if client:
            self.client = client
        else:
            self.client = requests.Session()

    def make_request(self, query, variables):
        for _ in range(3):  # Retry logic
            try:
                response = self.client.post(self.base_url, json={'query': query, 'variables': variables})
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Request failed with status code {response.status_code}. Retrying...")
                    time.sleep(3)  # Wait for 1 second before retrying
            except Exception as e:
                print(f"An error occurred: {e}. Retrying...")
                time.sleep(3)
        return None  # Return None if all retries fail

    def get_schedule_from_anilist(self):
        query = """
        query Q ($page: Int, $perPage: Int) {
          Page(page: $page, perPage: $perPage) {
            pageInfo {
              hasNextPage
            }
            media(sort: ID, type: ANIME, status_not_in: [NOT_YET_RELEASED, FINISHED]) {
              id
              idMal
              nextAiringEpisode {
                episode
                timeUntilAiring
                airingAt
              }
              coverImage {
                large
                extraLarge
              }
              title {
                userPreferred
                native
                romaji
              }
            }
          }
        }
        """

        results = []
        page = 1
        has_next_page = True

        while has_next_page:
            variables = {"page": page, "perPage": 100}
            data = self.make_request(query, variables)
            if data:
                # Filter out entries where nextAiringEpisode is not null
                filtered_media = [media for media in data['data']['Page']['media'] if media['nextAiringEpisode'] is not None]
                results.extend(filtered_media)
                has_next_page = data['data']['Page']['pageInfo']['hasNextPage']
                page += 1
            else:
                print("Failed to fetch data after 3 retries.")
                break
        print("Finished fetching data from AniList. total: ", len(results))
        return results

