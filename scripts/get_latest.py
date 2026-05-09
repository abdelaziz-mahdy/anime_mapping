import requests

from anilist_recent import AnilistRecent
from common import readJsonFile, writeJsonFileIfDifferent

mappingFile = "../latest.json"


def main():
    latest = readJsonFile(mappingFile)
    fetched = AnilistRecent(requests.Session()).get_recent_episodes(days_back=7)

    # Merge as monotonic max — never decrease a recorded episode
    # number. AniList sometimes reissues lower episode numbers for
    # specials / re-airings; ignoring those keeps the file aligned with
    # the latest broadcast actually in the wild.
    added = 0
    bumped = 0
    for mal_id, ep in fetched.items():
        cur = latest.get(mal_id)
        if cur is None:
            latest[mal_id] = ep
            added += 1
        elif isinstance(cur, (int, float)) and ep > cur:
            latest[mal_id] = ep
            bumped += 1

    print(f"Latest: +{added} new, {bumped} bumped, "
          f"{len(latest) - 1} total entries (incl. legacy)")
    writeJsonFileIfDifferent(mappingFile, latest)


if __name__ == "__main__":
    main()
