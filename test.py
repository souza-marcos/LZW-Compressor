from lzw import LZWCompressor

lzw = LZWCompressor()
lzw.compress("dijkstra.bmp", "dijkstra.lzw")
lzw.decompress("dijkstra.lzw", "dijkstra_dec.bmp")

# lzw.compress("test.txt", "test.lzw")
# lzw.decompress("test.lzw", "test_dec.txt")

# print(lzw.printDict())