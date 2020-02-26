'''
Created on Jan 7, 2020

@author: Daniel
'''

import json

if __name__ == '__main__':
    with open("fileTypes.json", "r") as file:
        jsonData = json.load(file)
    print(jsonData.get("7b5c72746631"))