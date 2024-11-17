from radixTree import radixTree 
from enum import Enum

class LZWMode(Enum):
    FIXED = 1
    VARIABLE = 2

class LZWCompressor:

    def __init__(self, mode : LZWMode = LZWMode.FIXED, limSizeCode : int = 12):
        if limSizeCode < 9:
            raise Exception("Tamanho do código deve ser de pelo menos 9 bits")

        self.dictionary = radixTree()
        self.mode = mode
        self.limSizeCode = limSizeCode

        self.sizeCode = 9 

        self.sizeBufferOut = 16         # Tamanho do buffer de saída, Deve ser multiplo de 8
        if mode == LZWMode.FIXED:
            self.sizeCode = limSizeCode

        self.clearCode = (1 << self.sizeCode) - 1
        

    def reinitDict(self):
        print(self.dictionary.manyWords) # LOG
        self.dictionary = radixTree()
        for i in range(256):    
            self.dictionary.insert(i.to_bytes(1, byteorder='big'), i)


    def compress(self, pathIn : str, pathOut : str):
        
        self.reinitDict()

        prefix = bytes()
        buffer = int(0)
        bufferSize = int(0)

        with open(pathIn, "rb") as fin, open(pathOut, "wb") as fout:
            nextchr = fin.read(1)
            while nextchr:
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
                if self.dictionary.manyWords == (1 << self.sizeCode) -1:
                    if prefix:
                        idx = self.dictionary.search(prefix).value
                        buffer = (buffer << self.sizeCode) | idx
                        bufferSize += self.sizeCode
                        prefix = bytes()
                    
                    buffer = (buffer << self.sizeCode) | self.clearCode 
                    bufferSize += self.sizeCode
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
                
        print("Qtd de palavras no dict:", self.dictionary.manyWords) # LOG


    def decompress(self, pathIn : str, pathOut : str):
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

    def printDict(self):
        self.dictionary.printTree()