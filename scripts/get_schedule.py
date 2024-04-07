from common import *
import cloudscraper
from anilist_schedule import AnilistSchedule
scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance

mappingFile="../schedule.json"

latest=readJsonFile(mappingFile)

jsonObject=AnilistSchedule(scraper).get_schedule_from_anilist()
print(jsonObject)

jsonObject={
    "__version__":latest.get("__version__",0),
    "data":jsonObject
}

writeJsonFileIfDifferent(mappingFile,jsonObject)
