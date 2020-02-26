import json

fileType = dict()

fileType = json.load(open("fileTypes.json"))

print(fileType)