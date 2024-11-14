import Trie


dictionary = Trie.Trie()
dictionary.insert('banana', 1)
dictionary.insert('bananas', 2)
dictionary.insert('bananinha', 3)
dictionary.insert('bananada', 4)
dictionary.insert('bana', 5)
dictionary.insert('banan', 6)           # Bug

print(dictionary.search('banana'))
print(dictionary.search('bananas'))
print(dictionary.search('bananinha'))
print(dictionary.search('bananada'))
print(dictionary.search('bana'))
print(dictionary.search('banan'))
print(dictionary.search('ban'))

dictionary.delete('bananada')
print(dictionary.search('bananada'))