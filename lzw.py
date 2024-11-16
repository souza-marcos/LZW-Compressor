from radixTree import radixTree 

class LZWCompressor:

    clearCode = 2**12 - 1

    def __init__(self):
        self.dictionary = radixTree()
        self.sizeCode = 12  # 12-bit code in the fixed variant
        self.sizeBufferOut = 16

    def reinitialize(self):
        print(self.dictionary.many_words)
        self.dictionary = radixTree()
        for i in range(256):    
            self.dictionary.insert(i.to_bytes(1, byteorder='big'), i)


    def compress(self, pathIn : str, pathOut : str):
        
        self.reinitialize()

        prefix = bytes()
        buffer = int(0)
        buffer_size = 0

        with open(pathIn, "rb") as fin, open(pathOut, "wb") as fout:
            nextchr = fin.read(1)
            while nextchr:
                combined = prefix + nextchr
                if not self.dictionary.search(combined):
                    self.dictionary.insert(combined, self.dictionary.many_words)

                    idx = self.dictionary.search(prefix)
                    if idx is None:
                        raise Exception("Prefix not found in dictionary")
                    
                    idx = idx.value

                    buffer = (buffer << self.sizeCode) | idx
                    buffer_size += self.sizeCode

                    while buffer_size >= self.sizeBufferOut:
                        toWrite = (buffer >> (buffer_size - self.sizeBufferOut)) & 0xFFFF
                        # print(type (toWrite), toWrite, buffer)
                        fout.write(toWrite.to_bytes(self.sizeBufferOut//8, byteorder='big'))
                        buffer_size -= self.sizeBufferOut
                        buffer = buffer & ((1 << buffer_size) - 1)
                    
                    prefix = nextchr
                
                else:
                    prefix = combined
                
                if self.dictionary.many_words == (2**self.sizeCode) -1:
                    if prefix:
                        idx = self.dictionary.search(prefix).value
                        buffer = (buffer << self.sizeCode) | idx
                        buffer_size += self.sizeCode
                    
                    buffer = (buffer << self.sizeCode) | ((2**self.sizeCode) - 1)   # Clear Code 
                    self.reinitialize()
                    

                nextchr = fin.read(1)

            if prefix:
                idx = self.dictionary.search(prefix).value
                buffer = (buffer << self.sizeCode) | idx
                buffer_size += self.sizeCode

            if(buffer_size > 0):
                while buffer_size >= self.sizeBufferOut:
                    toWrite = (buffer >> (buffer_size - self.sizeBufferOut)) & 0xFFFF
                    fout.write(toWrite.to_bytes(self.sizeBufferOut//8, byteorder='big'))
                    buffer_size -= self.sizeBufferOut
                    buffer = buffer & ((1 << buffer_size) - 1)
                
                # TODO: Critical, need to revisit
                toWrite = (buffer << (self.sizeBufferOut - buffer_size)) & 0xFFFF
                fout.write(toWrite.to_bytes(self.sizeBufferOut//8, byteorder='big'))

        print(self.dictionary.many_words)
        # self.printDict()
        # self.dictionary.print_inverted_list()


    def decompress(self, pathIn : str, pathOut : str):
        self.reinitialize()

        with open(pathIn, "rb") as fileIn, open(pathOut, "wb") as fileOut:

            buffer = 0
            buffer_size = 0

            def get_next_code():
                nonlocal buffer, buffer_size
                while buffer_size < self.sizeCode:
                    chunk = fileIn.read(2)
                    if not chunk:
                        return None
                    
                    buffer = (buffer << 16) | int.from_bytes(chunk, byteorder='big')
                    buffer_size += 16

                code = (buffer >> (buffer_size - self.sizeCode)) & ((1 << self.sizeCode) - 1)
                buffer_size -= self.sizeCode
                buffer = buffer & ((1 << buffer_size) - 1)
                return code

            def get_word(code):
                if code is None or code >= self.dictionary.many_words:
                    return None
                
                node = self.dictionary.indexTable[code]
                return self.dictionary.get_word(node)
                # if code is None or code >= self.dictionary.many_words:
                #     return None

                # return self.dictionary.indexTable[code].prefix  

            code = get_next_code()
            
            if code is None:
                return

            word = get_word(code)
            if word is None:
                raise Exception(f"Invalid code: {code}! At line 132")
            
            fileOut.write(word)
            previous_word = word

            while True:
                code = get_next_code()
                if code is None:
                    break

                if code == self.clearCode:
                    self.reinitialize()
                    code = get_next_code()
                    if code is None:
                        return
                    word = get_word(code)
                    if word is None:
                        raise Exception(f"Invalid code {code}! At line 149")

                    fileOut.write(word)
                    previous_word = word 
                    continue
                
                if code < self.dictionary.many_words:
                    word = get_word(code)
                    if word is None:
                        raise Exception(f"Invalid code! {code}")

                    fileOut.write(word)
                    self.dictionary.insert(previous_word + word[:1], self.dictionary.many_words)
                    previous_word = word

                else:
                    word = previous_word + previous_word[:1]
                    fileOut.write(word)
                    self.dictionary.insert(word, self.dictionary.many_words)
                    previous_word = word



    def printDict(self):
        self.dictionary.print_tree()