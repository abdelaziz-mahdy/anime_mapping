from common import *
import cloudscraper
from gogo_anime_parser import GogoAnimeParser

scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
domains=GogoAnimeParser(scraper).fetch_alternate_domains()

mappingFile="../domains.json"

latest=readJsonFile(mappingFile)
print("latest ", latest)
# add a condition to check if the domains already exist ignoring order
# latest domains is the current, domains variable is the new
latest["domains"]=list(set(latest["domains"]).union(set(domains)))
print("new latest ", latest)
# latest["domains"]=domains

writeJsonFileIfDifferent(mappingFile,latest)
