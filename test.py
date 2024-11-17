from lzw import LZWCompressor, LZWMode

lzw = LZWCompressor(mode=LZWMode.VARIABLE, limSizeCode=14)

print("Compressing...")
lzw.compress("./inputs/hollow.bmp", "./outputs/hollow.lzw")

print("Decompressing...")
lzw.decompress("./outputs/hollow.lzw", "./outputs/hollow_dec.bmp")
