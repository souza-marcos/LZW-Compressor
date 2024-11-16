from lzw import LZWCompressor

lzw = LZWCompressor()
lzw.compress("test.txt", "test.lzw")


lzw.decompress("test.lzw", "decompressed.txt")

# print(lzw.printDict())