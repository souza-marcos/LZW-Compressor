from radixTree import radixTree

radix = radixTree()

inputs = ['banana', 'bananas', 'bananinha', 'bananada', 'bana', 'banan']

it = 0
for el in inputs:
    radix.insert(el, it)
    it += 1

tests = ['banana', 'bananas', 'bananinha', 'bananada', 'bana', 'banan']

for test in tests:
    print(f"Testando {test}...")
    print(f"Valor: {radix.search(test)}")