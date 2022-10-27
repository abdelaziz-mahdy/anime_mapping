from pathlib import Path
import json as json
from typing import Union
import tqdm as tqdm
from git import Repo,RemoteProgress
import git

class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)

def cloneRepo(link,path):
    try:
        Path("./MAL-Sync-Backup-2/.git/index.lock").unlink()
    except:
        pass
    try:
        repo = git.Repo(path)
        o = repo.remotes.origin
        print("pulling repo",link)
        o.pull("master", progress=CloneProgress())
    except:
        print("cloning repo",link)
        Repo.clone_from(link, path, progress=CloneProgress())
MAL_Sync_Backup_folder="MAL-Sync-Backup-2"
cloneRepo("https://github.com/MALSync/MAL-Sync-Backup.git","MAL-Sync-Backup-2")  

myAnimeListDir = Path(f"./{MAL_Sync_Backup_folder}/data/myanimelist/anime")
gogoAnimeDir = Path(f"./{MAL_Sync_Backup_folder}/pages/gogoanime")
Map={}
for file in tqdm.tqdm(list(myAnimeListDir.iterdir())):
    if file.is_file():

        extension = file.suffix
        old_name = file.stem
        if "_index" != old_name:
            data = json.loads(file.read_bytes())
            #print(data)

            english_name=None
            if("Zoro" in data["Pages"]):
                english_name=data["Pages"]["Zoro"][list(data["Pages"]["Zoro"].keys())[0]]["title"]
            else:
                if len(data["altTitle"])!=0:
                    english_name=data["altTitle"][0]
            gogo_link=None

            if("Gogoanime" in data["Pages"]):
                for key in list(data["Pages"]["Gogoanime"].keys()):
                    if "dub" not in key.lower():
                        gogo_link=key

            if gogo_link:
                Map[data["id"]]={
                    "japanese_name":data["title"],
                    "english_name":english_name,
                    "image":data["image"],
                    "gogo_link":gogo_link
                }
                Map[gogo_link]={
                    "japanese_name":data["title"],
                    "english_name":english_name,
                    "image":data["image"],
                    "malid":data["id"]
                }
            
        #print(Map)
out_file = open("mapping.json", "w")
print(len(Map))
json.dump(Map,out_file)
