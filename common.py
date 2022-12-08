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
        return {}

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
        out_file = open(filePath, "w")
        json.dump(jsonData,out_file, indent=4)
        version=getJsonVersion(jsonData)
        writeVersionJson(filePath,version)

def writeVersionJson(filePath:str,version:int):
    out_file = open(f'{basename(filePath)}_version.json','w') 
    json.dump(getJsonMapForVersion(version),out_file, indent=4)

