class TrieNode:
    def __init__(self, text = '') -> None:
        self.text = text
        self.children = {}
        self.isTermination = False
        self.value : int = -1

class Trie:

    def __init__(self) -> None:
        self.root = TrieNode()

    def maxPrefix(self, s:str, t:str) -> int:
        minLen = min(len(s), len(t))
        for i in range(minLen):
            if s[i] != t[i]:
                return i
        return minLen

    # Has a bug
    def insert(self, word: str, value: int) -> None:
        node = self.root
        while word:

            if word[0] not in node.children:    # Cria um novo nó
                newNode = TrieNode(word)
                newNode.isTermination = True
                newNode.value = value
                node.children[word[0]] = newNode
                return
        
            nextNode = node.children[word[0]]
            prefixLen = self.maxPrefix(word, nextNode.text)

            if prefixLen == len(nextNode.text): # Continua a busca
                node = nextNode
                word = word[prefixLen:]

            else:
                # Quebra a aresta
                
                # Arruma o nó atual
                remainNode = TrieNode(nextNode.text[prefixLen:])
                remainNode.children = nextNode.children
                remainNode.isTermination = nextNode.isTermination
                remainNode.value = nextNode.value

                # Arruma o nó pai
                nextNode.text = nextNode.text[:prefixLen]
                nextNode.children = {remainNode.text[0]: remainNode}
                nextNode.isTermination = False
                nextNode.value = -1

                # Cria o novo nó
                remainingWord = word[prefixLen:]
                if remainingWord:
                    newNode = TrieNode(remainingWord)
                    newNode.isTermination = True
                    nextNode.children[remainingWord[0]] = newNode
                    newNode.value = value
                else:                                   # O texto acabou no meio do nó anterior
                    nextNode.isTermination = True
                    nextNode.value = value
                return

    def search(self, word: str) -> TrieNode | None:
        node = self.root
        while word:
            if word[0] not in node.children:
                return None
            nextNode = node.children[word[0]]
            prefixLen = self.maxPrefix(word, nextNode.text)
            if prefixLen == len(nextNode.text):
                node = nextNode
                word = word[prefixLen:]
            else:
                return None

        if node.isTermination:
            return node
        return None


    # Has a bug
    def delete(self, word: str) -> None:
        node = self.root
        while word:
            if word[0] not in node.children:
                return
            nextNode = node.children[word[0]]
            prefixLen = self.maxPrefix(word, nextNode.text)
            if prefixLen == len(nextNode.text):
                node = nextNode
                word = word[prefixLen:]
            else:
                return

        if node.isTermination:
            node.isTermination = False
            node.value = -1