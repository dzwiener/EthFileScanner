'''
Created on Jan 7, 2020

@author: Daniel Zwiener

@summary: For analyzing a string of data and comparing it to the file type database
'''


class FileTypeAnalyzer(object):
    '''
    classdocs
    '''
    __initString = ""
    __fileType = "None"
    
    
    def __init__(self, data):
        '''
        Constructor
        '''
        self.initString = data
        
        