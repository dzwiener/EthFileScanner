'''
Created on Jan 7, 2020

@author: Daniel Zwiener

@summary: For loading fileTypes from a .json file and returning a dictionary with the same information
'''

import json


class FileTypeLoader(object):
    '''
    classdocs
    '''
    __fileTypeDict = dict()
    __prefixSizes = set()
    __path = "fileTypes.json"
    
    '''
    @var path: path to a json file that contains a dict
    '''
    def __initJsonData(self):
        with open(self.__path, "r") as file:
            self.__fileTypeDict = json.load(file)
        
    
    def __detLen(self):
        for i in self.__fileTypeDict.keys():
            self.__prefixSizes.add(len(i))
    
    
    def __init__(self, pathToJson):
        '''
        Constructor
        '''
        print("Init")
        self.__path = pathToJson
        self.__initJsonData()
        self.__detLen()
        
    def getTypeDict(self):
        return self.__fileTypeDict

    def getSizeSet(self):
        return self.__prefixSizes