import time


class AnilistRecent:
    """Pulls recently aired episodes (in Japan) from AniList's
    `airingSchedules` endpoint within a `[now - days_back, now]` window.

    AniList's airing window is the broadcast time in Japan — an episode
    that aired today may not yet be uploaded to the user's streaming
    provider. The consumer (anime_here/background_checker.dart) words
    its notification accordingly. Use this as a "what aired" signal,
    not a "what's streamable" signal.
    """

    def __init__(self, client):
        self.base_url = "https://graphql.anilist.co"
        self.client = client

    def _request(self, query, variables):
        for _ in range(3):
            try:
                resp = self.client.post(
                    self.base_url,
                    json={"query": query, "variables": variables},
                )
                if resp.status_code == 200:
                    return resp.json()
                print(f"AniList status {resp.status_code}, retrying...")
                time.sleep(3)
            except Exception as e:
                print(f"AniList error: {e}, retrying...")
                time.sleep(3)
        raise Exception("AniList: all retries failed")

    def get_recent_episodes(self, days_back=7):
        """Returns `{idMal_str: highest_episode_int}` for every airing
        the API knows about within the window.

        idMal can be null on the AniList side (typically for OVAs/ONAs
        that aren't on MAL) — those entries are skipped, since the
        consumer keys exclusively by MAL id.
        """
        query = """
        query Q($page: Int, $perPage: Int, $g: Int, $l: Int) {
          Page(page: $page, perPage: $perPage) {
            pageInfo { hasNextPage }
            airingSchedules(
              airingAt_greater: $g,
              airingAt_lesser: $l,
              sort: TIME_DESC
            ) {
              episode
              media { idMal }
            }
          }
        }
        """
        now = int(time.time())
        lower = now - days_back * 86400
        out = {}
        page = 1
        while True:
            data = self._request(
                query,
                {"page": page, "perPage": 50, "g": lower, "l": now},
            )
            if not data or "data" not in data:
                break
            page_data = data["data"]["Page"]
            for s in page_data["airingSchedules"]:
                media = s.get("media") or {}
                mal_id = media.get("idMal")
                ep = s.get("episode")
                if mal_id is None or ep is None:
                    continue
                key = str(mal_id)
                if key not in out or ep > out[key]:
                    out[key] = ep
            if not page_data["pageInfo"]["hasNextPage"]:
                break
            page += 1
            # AniList's documented limit is 90 req/min; pace ourselves
            # to leave headroom for the schedule.yml job that shares
            # this API.
            time.sleep(0.7)
        print(f"AniList recent: {len(out)} shows aired in last {days_back}d")
        return out
