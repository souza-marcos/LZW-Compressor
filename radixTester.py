from radixTree import radixTree

radix = radixTree()

inputs = [b'banana', b'bananas', b'bananinha', b'bananada', b'bana', b'banan', b'b']

it = 0
for el in inputs:
    radix.insert(el, it)
    it += 1

tests = [b'banana', b'bananas', b'bananinha', b'bananada', b'bana', b'banan', b'casca']

for test in tests:
    print(f"Testando {test.decode('utf-8')}...")
    node = radix.search(test)
    print(f"Valor: {'VOID' if node is None else node.value}")

radix.print_tree()
