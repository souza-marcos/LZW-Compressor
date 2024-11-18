import time 
import os
import argparse
from lzw import LZWCompressor, LZWMode 

# Main Code for handle scripting, cli args, etc

def compress(input, output, variant, limSizeCode, stats):
    startTime = time.perf_counter()
    
    mode = LZWMode.VARIABLE if variant == "variable" else LZWMode.FIXED
    limSizeCode = limSizeCode if limSizeCode else 12

    lzw = LZWCompressor(mode, limSizeCode)
    lzw.compress(input, output)
    
    
    totalTime = (time.perf_counter() - startTime) * 1e3
    
    if stats:
        originalSize = os.path.getsize(input)
        compressedSize = os.path.getsize(output)
        compressionRatio = compressedSize/originalSize
        with open("stats.txt", "a") as f:
            f.write(f"1 {lzw.memoryDict/1000} {lzw.wordsAdded} {totalTime} {0 if mode == LZWMode.FIXED else 1} {limSizeCode} {originalSize} {compressedSize} {compressionRatio}\n")
            

def decompress(input, output, variant, limSizeCode, stats):
    startTime = time.perf_counter()
    
    mode = LZWMode.VARIABLE if variant == "variable" else LZWMode.FIXED
    limSizeCode = limSizeCode if limSizeCode else 12

    lzw = LZWCompressor(mode, limSizeCode)
    lzw.decompress(input, output)
    
    totalTime = (time.perf_counter() - startTime) / 1e3
    
    if stats:
        with open("stats.txt", "a") as f:
            f.write(f"0 {lzw.memoryDict/1000} {lzw.wordsAdded} {totalTime} {0 if mode == LZWMode.FIXED else 1} {limSizeCode} 0 0 0\n")


def main():
    parser = argparse.ArgumentParser(description="Ferramenta de compressão/descompressão de dados usando LZW")
    parser.add_argument("--mode", required=True, choices=["compress", "decompress"], help="Modo de operação: compressão ou descompressão")
    parser.add_argument("input", help="Arquivo de entrada para compressão/descompressão em formato não comprimido")
    parser.add_argument("output", help="Arquivo de saída para compressão/descompressão em formato comprimido")
    parser.add_argument("--stats", required=False, action="store_true", help="Salvar estatísticas")
    parser.add_argument("--variant", required=False, choices=["fixed", "variable"], help="Código do compressão deve ser fixo ou variável")
    parser.add_argument("--maxbits", type=int, help="Número máximo de bits para o código de compressão, deve ser maior que 8. Padrão: 12")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found!")
        return
    
    if args.mode == "compress":
        compress(args.input, args.output, args.variant, args.maxbits, args.stats)

    elif args.mode == "decompress":
        decompress(args.input, args.output, args.variant, args.maxbits, args.stats)

    else:
        print("Modo inválido. Use '--mode compress' ou '--mode decompress'")


if __name__ == "__main__":
    main()