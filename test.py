from lzw import LZWCompressor, LZWMode

lzw = LZWCompressor(mode=LZWMode.VARIABLE, limSizeCode=14)

print("Compressing...")
lzw.compress("./inputs/test.txt", "./outputs/test.lzw")

print("Decompressing...")
lzw.decompress("./outputs/test.lzw", "./outputs/test_dec.txt")
