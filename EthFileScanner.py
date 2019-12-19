'''
Created on Dec 12, 2019

@author: Daniel
'''
from web3 import Web3, HTTPProvider
import os, sys

#TODO implement a configuration file


version = "1.1.1"
#Required variables
httpAddress = "http://127.0.0.1:8545"

w3 = Web3(HTTPProvider(httpAddress))
hexEncoding = "ISO-8859-1"

topDir = "EthFiles"

filePrefixes = dict()
sizesOfPrefixes = set()

"""
Purpose
    Checks if the node is ready to start parsing for files
"""
def checkNode():
    print("Checking node now...")
    if(w3.isConnected()):
        print("Connected")
    else:
        print("Node is not connected properly. Please try changing the address or checking that your node's HTTP functionality is turned on")
        return 1
    if(not w3.eth.syncing):
        #TODO find a way to identify the most current block
        print("Warning! Node is not fully synced. Data may not be current. Block height is at: ", w3.eth.blockNumber, " Expected: ", "TODO")
    return 0;

'''
Purpose
    Displays information on a certain block
Parameters
    blockNum: Block passed into this method
    verbose: Indicates how much detail you want in the console
'''
def displayInfo(blockNum, verbose=0):
    if(verbose < 2):
        print('Block: ', blockNum)
        print('Transactions: ', w3.eth.getBlock(blockNum).transactions)
    #TODO Implement further debugging information

'''
Purpose
    Fills a dict with each prefix for a file type and assigns the file type to that prefix
    Also sizeOfPrefixes is used to grab subStrings of data to avoid redundancy
'''
def initalizeFileCheck():
    filePrefixes = dict([
        ("ffd8", "jpeg"),
        ("ffe", "mp3"),
        ("fff", "mp3"),
        ("504b", "zip"),
        ("89504e470d0a1a0a", "png"),
        ("25504446", "pdf"),
        ("47494638", "gif"),
        ("4d5a", "exe"),
        ("526172211a07", "rar"),
        ("efbbbf", "txt"),
        ("4e45531a", "nes"),
        ("7b5c72746631", "rtf")
        ])
    for i in filePrefixes.keys():
        sizesOfPrefixes.add(i.__len__())


'''
Purpose
    Uses the dict established in initalizeFileCheck and sees if data matches the patterns in the dict
    if it does, return the file extension, which will be placed at the end of the file after the .
Parameters
    data: the extra data in a transaction that is potentially a file
'''
def checkForFile(data):
    """
    threes: ffe, fff
    fours: ffd8, 504b, 4d5a
    sixes: efbbbf
    """
    prefixes = []
    fileType = "None"
    for i in sizesOfPrefixes:
        prefixes.append(data.toString(2, i + 2))
    for i in prefixes:
        if(not filePrefixes.get(i, "None") == "None"):
            fileType = filePrefixes.get(i, "ERROR!")
    return fileType

'''
Purpose
    Takes a byteString and prints it to a file
Parameters
    byteString: a string containing a hex representation of a file
    fileName: will be the transaction hash, for easier searching
    block: is used to create the folder that the files will go into, for easier searching
'''
def printByteToFile(byteString, fileName, block):
    dirPath = topDir + "/" + str(block)
    path = dirPath + '/' + str(fileName)
    
    if(not os.path.exists(dirPath)):
        os.mkdir(dirPath)
        
    file = open(path, mode='w', encoding=hexEncoding)
    hexStr = byteString[2:]
    file.write(bytes.fromhex(hexStr).decode(hexEncoding))
    file.close()

if __name__ == '__main__':
    print(version)
    initalizeFileCheck()
    if(checkNode() == 1):
        print("GoodBye")
        sys.exit()
    if(not os.path.exists(topDir)):
        os.mkdir(topDir)
        
    startingBlock = 0
    #TODO, accurately determine number of blocks to parse
    numberOfBlocks = 8000000
    
    for i in range(startingBlock, startingBlock+numberOfBlocks):
        for transactionHash in w3.eth.getBlock(i).transactions:
            inputData = w3.eth.getTransaction(transactionHash).input
            #If no input assigned to transaction don't bother scanning it for file info
            if(not inputData == '0x'):
                fileType = checkForFile(inputData)
                if(not fileType == ""):
                    print(fileType, " ", inputData)
                    fileName = str((transactionHash.hex())) + '.' + str(fileType)
                    print(fileName)
                    printByteToFile(inputData, fileName, i)
    pass