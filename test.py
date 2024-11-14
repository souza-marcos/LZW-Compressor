pathIn = 'dijkstra.bmp'
pathOut = 'test.lzw'

def encode():

    dict = { bytes([i]): i for i in range(256) }
    nextIndex = 256

    with open(pathIn, 'rb') as fileIn:
        with open(pathOut, 'wb') as fileOut:
            byte = fileIn.read(1)
            if not byte:
                return   

            word = byte
            while True:
                byte = fileIn.read(1)
                if not byte:
                    break

                curVal = dict[word]

                word += byte
                if word in dict:
                    continue

                dict[word] = nextIndex
                nextIndex += 1


                fileOut.write(curVal.to_bytes(2, 'big'))
                word = byte

            if word:
                fileOut.write(dict[word].to_bytes(2, 'big'))

    print('Encoded')


def decode():
    dict = { i: bytes([i]) for i in range(256) }
    nextIndex = 0

    with open(pathIn, 'rb') as fileIn:
        with open(pathOut, 'wb') as fileOut:
            word = int.from_bytes(fileIn.read(2), 'big')
            fileOut.write(dict[word])

            while True:
                byte = fileIn.read(2)
                if not byte:
                    break

                if int.from_bytes(byte, 'big') in dict:
                    word = int.from_bytes(byte, 'big')
                    fileOut.write(dict[word])
                    continue

                dict[nextIndex] = dict[word] + dict[word][0:1]
                nextIndex += 1
                fileOut.write(dict[word])

    print('Decoded')

encode()

pathIn = pathOut
pathOut = 'decoded.bmp'

decode()