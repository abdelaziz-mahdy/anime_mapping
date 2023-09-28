from common import *
import cloudscraper
from gogo_anime_parser import GogoAnimeParser

scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
domains=GogoAnimeParser(scraper).fetch_alternate_domains()

mappingFile="../domains.json"

latest=readJsonFile(mappingFile)
print("latest ", latest)
latest["domains"]=domains

writeJsonFileIfDifferent(mappingFile,latest)
