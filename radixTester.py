from radixTree import radixTree

radix = radixTree()

inputs = [b'banana', b'bananas', b'bananinha', b'bananada', b'bana', b'banan', b'bica']


for el in inputs:
    radix.insert(el, radix.manyWords)

tests = [b'banana', b'bananas', b'bananinha', b'bananada', b'bana', b'banan', b'casca']

for test in tests:
    print(f"Testando {test.decode('utf-8')}...")
    node = radix.search(test)
    print(f"Valor: {'VOID' if node is None else node.value}")

radix.printTree()
radix.printInvertedList()