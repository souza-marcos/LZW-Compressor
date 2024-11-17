class radixNode:
    def __init__(self, prefix: bytearray = "", isLeaf: bool = False, value: int = None):
        # Prefixo associado a este node
        self.prefix = prefix

        # Flag que sinaliza se existe o node é uma folha
        self.isLeaf = isLeaf
        self.value = value
        self.parent = None

        # Dicionário que mapeia nodes filhos de acordo com o primeiro caracter dos prefixos
        self.children: dict[bytes, radixNode] = {}
    
    def commonPrefixLenght(self, str1, str2):
        length = 0
        maxLength = min(len(str1),len(str2))
        for i in range(maxLength):
            if str1[i:(i+1)] != str2[i:(i+1)]:
                break
            length = length + 1
        return length

class radixTree:
    def __init__(self):
        # Raiz da árvore
        self.root = radixNode()
        self.indexTable  = [] # Lista invertida Código -> Nó

        # Quantidade de palavras inseridas na árvore
        self.manyWords = 0

    def insert(self, word, value: int):
        """Insere uma palavra na árvore radix"""
        if not word:
            if not self.root.isLeaf:
                self.manyWords += 1
            self.root.isLeaf = True
            self.root.value = value
            self.indexTable.append(self.root)
            return

        self.manyWords += 1
        curNode = self.root
        # Verificando prefixos em comum entre os filhos
        while word:
            if not curNode.children:
                newNode = radixNode(word, True, value)
                curNode.children[word[0:1]] = newNode 
                newNode.parent = curNode
                self.indexTable.append(newNode)
                return

            for _, child in curNode.children.items():
                commonPrefixLength = curNode.commonPrefixLenght(word, child.prefix)
                
                # Caso exista um filho com prefixo em comum
                if commonPrefixLength > 0:
                    # Se o prefixo do node filho precisa ser dividido
                    if commonPrefixLength < len(child.prefix):
                        # O node filho é divido
                        splitNode = radixNode(child.prefix[commonPrefixLength:])
                        splitNode.children = child.children
                        splitNode.isLeaf = child.isLeaf
                        splitNode.value = child.value
                        splitNode.parent = child

                        if child.value is not None: 
                            self.indexTable[child.value] = splitNode

                        # Node filho é atualizado
                        child.prefix = child.prefix[:commonPrefixLength]
                        child.children = {splitNode.prefix[0:1] : splitNode}
                        child.isLeaf = False
                        child.value = None
                    
                    # Continua o processo com o resto do prefixo de 'word' no nó filho
                    word = word[commonPrefixLength:]
                    curNode = child
                    break
            # Caso nenhum prefixo em comum seja encontrado: adiciona novo filho
            else:
                newNode = radixNode(word, True, value)
                curNode.children[word[0:1]] = newNode
                newNode.parent = curNode
                self.indexTable.append(newNode)
                return
            
        print("Erro: palavra já inserida")
        curNode.isLeaf = True
        curNode.value = value
        self.indexTable[value] = curNode
    
    def search(self, word) -> radixNode:
        """Busca uma palavra na árvore radix"""
        curNode = self.root
        while word:
            found = False
            for _, child in curNode.children.items():
                commonPrefixLength = curNode.commonPrefixLenght(word, child.prefix)
                if commonPrefixLength > 0:
                    word = word[commonPrefixLength:]
                    curNode = child
                    found = True
                    break
            if not found:
                return None
            
        #True #se a palavra tem que obrigatoriamente ter sido inserida: curNode.isLeaf    
        return curNode if curNode.isLeaf else None
    
    def remove(self, word: str):
        """Remove uma palavra da árvore radix. Retorna True se a remoção foi bem-sucedida."""
        return self._remove(self.root, word)

    def _remove(self, node: radixNode, word: str) -> bool:
        """Função auxiliar recursiva para remover uma palavra da árvore radix."""
        if not word:
            # Se a palavra está vazia, chegamos ao fim da palavra a ser removida
            if node.isLeaf:
                node.isLeaf = False  # Desmarca o nó como folha
                # Verifica se o nó não tem filhos para possivelmente removê-lo
                return len(node.children) == 0  # Retorna True se o nó pode ser removido
            return False  # A palavra não estava presente

        # Percorre os filhos procurando o próximo prefixo
        for key, child in node.children.items():
            commonPrefixLength = node.commonPrefixLenght(word, child.prefix)
            if commonPrefixLength == len(child.prefix):
                # A parte correspondente do prefixo foi encontrada
                if self._remove(child, word[commonPrefixLength:]):
                    # Remove o nó filho se ele estiver vazio e não for uma folha
                    del node.children[key]

                    # Após remover o filho, verifica se o nó atual ainda precisa existir
                    return not node.isLeaf and len(node.children) == 0
                return False
        return False
    
    def printTree(self):
        def _printNode(node : radixNode, prefix=""):
            # Imprime o prefixo atual e se é uma folha
            isLeaf = f"(folha) => {node.value} " if node.isLeaf else ""
            print(f"{prefix}{node.prefix} {isLeaf} {node.parent.value if node.parent is not None else "NONE"}" )

            # Percorre recursivamente os filhos
            for child in node.children.values():
                _printNode(child, prefix + "  ")

        # Inicia a impressão a partir da raiz
        _printNode(self.root)

    def getWord(self, curNode):
        word = bytearray()
        while curNode and curNode.parent:
            word = curNode.prefix + word
            curNode = curNode.parent
        return word

    def printInvertedList(self):
        for it, elem in enumerate(self.indexTable):
            if elem is None:
                print(it, ": None") 
            else:
                print(it, ":", self.getWord(elem))

            if it >= self.manyWords:
                break