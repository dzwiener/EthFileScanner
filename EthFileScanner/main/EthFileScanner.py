'''
Created on Dec 12, 2019

@author: Daniel Zwiener
'''
import os, sys

from web3 import Web3, HTTPProvider
from FileTypeLoader import FileTypeLoader
from web3.providers.ipc import IPCProvider


#TODO implement a configuration file
version = "1.2.0"

#Required variables
w3 = Web3(IPCProvider())
hexEncoding = "ISO-8859-1"

topDir = "EthFiles"
sizesOfPrefixes = set()

#Counters:
numberOfBlocks = 0
numberOfTransactions = 0
numberOfDataTransactions = 0
numberOfFiles = 0

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
    if(w3.eth.syncing):
        #TODO find a way to identify the most current block
        print("Warning! Node is not fully synced. Data may not be current. Block height is at: ", w3.eth.syncing.currentBlock, " Expected: ", w3.eth.syncing.highestBlock)
    return 0;

'''
Purpose
    Displays information on a certain block
Parameters
    blockNum: Block passed into this method
    verbose: Indicates how much detail you want in the console
'''
def displayInfo(blockNum, verbose=0):
    output = '[INFO] '
    if(verbose <= 2):
#         output = output, "Blocks scanned so far: ", numberOfBlocks, " Currently scanning block: ", blockNum
        output = output + 'Blocks scanned so far: %010d Currently scanning block: %010d ' % (numberOfBlocks, blockNum)
    if(verbose <= 1):
#         output = output, "Transactions so far: ", numberOfTransactions, "Files So far: ", numberOfFiles, "Transactions with data so far: ", numberOfDataTransactions
        output = output + 'Transactions so far: %010d Files So far: %010d Transactions with data so far:  %010d' % (numberOfTransactions, numberOfFiles, numberOfDataTransactions)
    if(verbose == 0):
        pass
    print(output)
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
    for i in sizeOfPrefixes:
        prefixes.append(data[2:(i + 2)])
    for i in prefixes:
        if(not fileLoader.getTypeDict().get(i, fileType) == fileType):
            fileType = fileLoader.getTypeDict().get(i, "ERROR!")
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
    if(not os.path.exists(topDir)):
        os.mkdir(topDir)
    
    if(not os.path.exists(dirPath)):
        os.mkdir(dirPath)
        
    file = open(path, mode='w', encoding=hexEncoding)
    hexStr = byteString[2:]
    file.write(bytes.fromhex(hexStr).decode(hexEncoding))
    file.close()

if __name__ == '__main__':
    print(version)
    fileLoader = FileTypeLoader("fileTypes.json")
    sizeOfPrefixes = fileLoader.getSizeSet()
    if(checkNode() == 1):
        print("GoodBye")
        sys.exit()
    
    startingBlock  = 0
    #TODO, accurately determine number of blocks to parse
    numberOfBlocksToScan = 10000000
    
    print("Starting Scan")
    #Goes through each block in the range provided
    for i in range(startingBlock, startingBlock+numberOfBlocksToScan):
        #Reports constantly on the scanning for files
        if(i % 100 == 0):
            displayInfo(i, verbose=1)
        
        #Goes through each transaction in this block
        for transactionHash in w3.eth.getBlock(i).transactions:
            inputData = w3.eth.getTransaction(transactionHash).input
            #If no input assigned to transaction don't bother scanning it for file info
            if(not inputData == '0x'):
                fileType = checkForFile(inputData)
                if(not fileType == "None"):
                    fileName = str((transactionHash.hex())) + '.' + str(fileType)
                    print("[FILE]", fileName, " ", inputData, " ", fileType)
                    printByteToFile(inputData, fileName, i)
                    numberOfFiles = numberOfFiles + 1
                numberOfDataTransactions = numberOfDataTransactions + 1
            numberOfTransactions = numberOfTransactions + 1
        numberOfBlocks = numberOfBlocks + 1
    pass