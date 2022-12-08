from pathlib import Path
import json as json
import jsondiff

versionKey="__version__"
def basename(path):
    return Path(path).stem

def indexOfLastCharacterOfSubstring(string,substring):
    return string.index(substring)+len(substring)

def readJsonFile(filePath:str):
    try:
        return json.loads(Path(filePath).read_bytes())
    except:
        return getJsonMapForVersion(0)

def getJsonVersion(jsonData:dict):
    return jsonData.get(versionKey,0)

def getJsonMapForVersion(version:int):
    return {versionKey:version}

def incrementJsonVersion(jsonData:dict):
    jsonData[versionKey]=jsonData.get(versionKey,0)+1
    return jsonData

def writeJsonFileIfDifferent(filePath:str,jsonData:dict):
    oldJson=readJsonFile(filePath)
    res = jsondiff.diff(oldJson, jsonData)
    if res:        
        print("Diff found")
        jsonData=incrementJsonVersion(jsonData)
        with open(filePath,'w') as f:
            json.dump(jsonData,f, indent=4)
        version=getJsonVersion(jsonData)
        writeVersionJson(filePath,version)

def writeVersionJson(filePath:str,version:int):
    with open(f'{basename(filePath)}_version.json','w')  as f:
        json.dump(getJsonMapForVersion(version),f, indent=4)
