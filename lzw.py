from radixTree import radixTree 
from enum import Enum
import sys
import os

class LZWMode(Enum):
    FIXED = 1
    VARIABLE = 2

class LZWCompressor:

    def __init__(self, mode : LZWMode = LZWMode.FIXED, limSizeCode : int = 12):
        if limSizeCode < 9:
            raise Exception("Tamanho do código deve ser de pelo menos 9 bits")

        self.wordsAdded = 0
        self.memoryDict = 0
        self.curByte = 0

        self.dictionary = radixTree()
        self.mode = mode
        self.limSizeCode = limSizeCode

        self.sizeCode = 9 

        self.sizeBufferOut = 16         # Tamanho do buffer de saída, Deve ser multiplo de 8
        if mode == LZWMode.FIXED:
            self.sizeCode = limSizeCode

        self.clearCode = (1 << self.sizeCode) - 1
        

    def reinitDict(self):
        self.memoryDict += sys.getsizeof(self.dictionary)   # Stats
        self.wordsAdded += self.dictionary.manyWords        # Stats
        self.dictionary = radixTree()
        for i in range(256):    
            self.dictionary.insert(i.to_bytes(1, byteorder='big'), i)


    def compress(self, pathIn : str, pathOut : str):
        self.fileInSize = os.path.getsize(pathIn)
        self.curByte = 0
        self.curPercent = 0

        self.memoryDict = 0
        self.wordsAdded = 0

        self.sizeCode = 9 
        if self.mode == LZWMode.FIXED:
            self.sizeCode = self.limSizeCode

        self.clearCode = (1 << self.sizeCode) - 1

        self.reinitDict()

        prefix = bytes()
        buffer = int(0)
        bufferSize = int(0)

        with open(pathIn, "rb") as fin, open(pathOut, "wb") as fout:
            nextchr = fin.read(1)

            while nextchr:

                self.curByte += 1
                if self.curByte * 10 / self.fileInSize > self.curPercent:
                    self.curPercent += 1
                    print(f"Compressing... {self.curPercent * 10}%")

                combined = prefix + nextchr
                if not self.dictionary.search(combined):
                    self.dictionary.insert(combined, self.dictionary.manyWords)

                    idx = self.dictionary.search(prefix)
                    if idx is None:
                        raise Exception("Internal error while compressing: Prefix not found in dict!")
                    
                    idx = idx.value

                    buffer = (buffer << self.sizeCode) | idx
                    bufferSize += self.sizeCode

                    while bufferSize >= self.sizeBufferOut:
                        toWrite = (buffer >> (bufferSize - self.sizeBufferOut)) & ((1 << self.sizeBufferOut) - 1)
                        fout.write(toWrite.to_bytes(self.sizeBufferOut//8, byteorder='big'))
                        bufferSize -= self.sizeBufferOut
                        buffer = buffer & ((1 << bufferSize) - 1)
                    
                    prefix = nextchr
                
                else:
                    prefix = combined
                
                # Quando o dicionário estiver cheio
                if self.dictionary.manyWords >= (1 << self.sizeCode) -1:
                    
                    if prefix:
                        idx = self.dictionary.search(prefix).value
                        buffer = (buffer << self.sizeCode) | idx
                        bufferSize += self.sizeCode
                        prefix = bytes()

                    buffer = (buffer << self.sizeCode) | self.clearCode 
                    bufferSize += self.sizeCode

                    if self.sizeCode < self.limSizeCode:
                        self.sizeCode += 1
                        self.clearCode = (1 << self.sizeCode) - 1
                    # Dicionário cheio e tamanho do código no limite
                    else:       
                        self.reinitDict()

                nextchr = fin.read(1)

            if prefix:
                idx = self.dictionary.search(prefix).value
                buffer = (buffer << self.sizeCode) | idx
                bufferSize += self.sizeCode

            if(bufferSize > 0):
                while bufferSize >= self.sizeBufferOut:
                    toWrite = (buffer >> (bufferSize - self.sizeBufferOut)) & ((1 << self.sizeBufferOut) - 1)
                    fout.write(toWrite.to_bytes(self.sizeBufferOut//8, byteorder='big'))
                    bufferSize -= self.sizeBufferOut
                    buffer = buffer & ((1 << bufferSize) - 1)
                
                if bufferSize > 0:
                    toWrite = (buffer << (self.sizeBufferOut - bufferSize)) & ((1 << self.sizeBufferOut) - 1)
                    fout.write(toWrite.to_bytes(self.sizeBufferOut//8, byteorder='big'))
                
        self.wordsAdded += self.dictionary.manyWords        # Stats
        self.memoryDict += sys.getsizeof(self.dictionary)   # Stats


    def decompress(self, pathIn : str, pathOut : str):

        self.curByte = 0
        self.curPercent = 0
        self.fileInSize = os.path.getsize(pathIn)
        self.memoryDict = 0
        self.wordsAdded = 0

        self.sizeCode = 9 
        if self.mode == LZWMode.FIXED:
            self.sizeCode = self.limSizeCode

        self.clearCode = (1 << self.sizeCode) - 1
        
        self.reinitDict()

        with open(pathIn, "rb") as fileIn, open(pathOut, "wb") as fileOut:

            buffer = 0
            bufferSize = 0

            def getNextCode():
                nonlocal buffer, bufferSize
                while bufferSize < self.sizeCode:
                    chunk = fileIn.read(2)
                    if not chunk:
                        break
                    
                    self.curByte += 2
                    if self.curByte * 10 / self.fileInSize > self.curPercent:
                        self.curPercent += 1
                        print(f"Decompressing... {self.curPercent * 10}%")

                    buffer = (buffer << 16) | int.from_bytes(chunk, byteorder='big')
                    bufferSize += 16

                if bufferSize < self.sizeCode: 
                    bufferSize = 0
                    return None
                
                code = (buffer >> (bufferSize - self.sizeCode)) & ((1 << self.sizeCode) - 1)
                bufferSize -= self.sizeCode
                buffer = buffer & ((1 << bufferSize) - 1)
                return code

            def getWord(code):
                if code is None or code >= self.dictionary.manyWords:
                    return None
                
                node = self.dictionary.indexTable[code]
                return self.dictionary.getWord(node)
                
            code = getNextCode()
            
            if code is None:
                return

            word = getWord(code)
            if word is None:
                raise Exception(f"Internal error while decompressing: Invalid code: {code}!")
            
            fileOut.write(word)
            previousWord = word

            while True:
                code = getNextCode()
                if code is None: # Maybe EOF or flush the remaining bits
                    break

                if code == self.clearCode:

                    if self.sizeCode < self.limSizeCode:
                        self.sizeCode += 1
                        self.clearCode = (1 << self.sizeCode) - 1

                    else:
                        self.reinitDict()
                    
                    code = getNextCode()
                    if code is None:
                        return
                    word = getWord(code)
                    if word is None:
                        raise Exception(f"Internal error while decompressing: Invalid code: {code}!")
                    
                    fileOut.write(word)
                    previousWord = word 
                    continue
                
                if code < self.dictionary.manyWords:
                    word = getWord(code)
                    if word is None:
                        raise Exception(f"Internal error while decompressing: Invalid code: {code}!")
                    
                    fileOut.write(word)
                    self.dictionary.insert(previousWord + word[:1], self.dictionary.manyWords)
                    previousWord = word

                else:
                    word = previousWord + previousWord[:1]
                    fileOut.write(word)
                    self.dictionary.insert(word, self.dictionary.manyWords)
                    previousWord = word

        self.wordsAdded += self.dictionary.manyWords        # Stats
        self.memoryDict += sys.getsizeof(self.dictionary)

    def printDict(self):
        self.dictionary.printTree()