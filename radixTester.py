from radixTree import radixTree

radix = radixTree()
radix.insert('banana')
radix.insert('bananas')
radix.insert('bananinha')
radix.insert('bananada')
radix.insert('bana')
radix.insert('banan')

radix.remove('bananada')

print(radix.search('banana'))
print(radix.search('bananas'))
print(radix.search('bananinha'))
print(radix.search('bananada'))
print(radix.search('bana'))
print(radix.search('banan'))