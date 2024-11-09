from common import *
import cloudscraper
from gogo_anime_parser import GogoAnimeParser

scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
domains=GogoAnimeParser(scraper).fetch_alternate_domains()

mappingFile="../domains.json"

latest=readJsonFile(mappingFile)
print("latest json ", latest)
print("domains ", domains)
# add a condition to check if the domains already exist ignoring order
# latest domains is the current, domains variable is the new
# Get the current domains
current_domains = latest.get('domains', [])

# Update the list with new domains, preserving order and avoiding duplicates
updated_domains = current_domains.copy()
for domain in domains:
    if domain not in current_domains:
        updated_domains.append(domain)
# # sort the updated domains to make anything with gogo in it at the top
# updated_domains.sort(key=lambda x: x.lower().find("gogo") if x.lower().find("gogo") != -1 else 999999999999999999, reverse=False)
# Check if there are any new domains
print("current domains ", current_domains)
print("updated domains ", updated_domains)
if updated_domains != current_domains:
    # Update the domains in the 'latest' dictionary
    latest['domains'] = updated_domains
# latest["domains"]=domains

    print("Domains updated.")
else:
    print("Domains match, no update needed.")
writeJsonFileIfDifferent(mappingFile,latest)
