class radixNode:
    def __init__(self, prefix: bytearray = "", is_leaf: bool = False, value: int = None):
        # Prefixo associado a este node
        self.prefix = prefix

        # Flag que sinaliza se existe o node é uma folha
        self.is_leaf = is_leaf
        self.value = value
        self.parent = None

        # Dicionário que mapeia nodes filhos de acordo com o primeiro caracter dos prefixos
        self.children: dict[bytes, radixNode] = {}
    
    def _common_prefix_lenght(self, str1, str2):
        length = 0
        max_length = min(len(str1),len(str2))
        for i in range(max_length):
            if str1[i:(i+1)] != str2[i:(i+1)]:
                break
            length = length + 1
        return length

class radixTree:
    def __init__(self):
        # Raiz da árvore
        self.root = radixNode()
        self.indexTable  = [None] * 4096 

        # Quantidade de palavras inseridas na árvore
        self.many_words = 0

    def insert(self, word, value: int):
        """Insere uma palavra na árvore radix"""
        if not word:
            if not self.root.is_leaf:
                self.many_words += 1
            self.root.is_leaf = True
            self.root.value = value
            self.indexTable[value] = self.root
            return

        self.many_words += 1
        current_node = self.root
        # Verificando prefixos em comum entre os filhos
        while word:
            if not current_node.children:
                new_node = radixNode(word, True, value)
                current_node.children[word[0:1]] = new_node 
                new_node.parent = current_node
                self.indexTable[value] = new_node
                return

            for _, child in current_node.children.items():
                common_prefix_length = current_node._common_prefix_lenght(word, child.prefix)
                
                # Caso exista um filho com prefixo em comum
                if common_prefix_length > 0:
                    # Se o prefixo do node filho precisa ser dividido
                    if common_prefix_length < len(child.prefix):
                        # O node filho é divido
                        split_node = radixNode(child.prefix[common_prefix_length:])
                        split_node.children = child.children
                        split_node.is_leaf = child.is_leaf
                        split_node.value = child.value
                        split_node.parent = child

                        if child.value is not None: 
                            self.indexTable[child.value] = split_node

                        # Node filho é atualizado
                        child.prefix = child.prefix[:common_prefix_length]
                        child.children = {split_node.prefix[0:1] : split_node}
                        child.is_leaf = False
                        child.value = None
                    
                    # Continua o processo com o resto do prefixo de 'word' no nó filho
                    word = word[common_prefix_length:]
                    current_node = child
                    break
            # Caso nenhum prefixo em comum seja encontrado: adiciona novo filho
            else:
                new_node = radixNode(word, True, value)
                current_node.children[word[0:1]] = new_node
                new_node.parent = current_node
                self.indexTable[value] = new_node
                return
            
        print("Erro: palavra já inserida")
        current_node.is_leaf = True
        current_node.value = value
        self.indexTable[value] = current_node
    
    def search(self, word) -> radixNode:
        """Busca uma palavra na árvore radix"""
        current_node = self.root
        while word:
            found = False
            for _, child in current_node.children.items():
                common_prefix_len = current_node._common_prefix_lenght(word, child.prefix)
                if common_prefix_len > 0:
                    word = word[common_prefix_len:]
                    current_node = child
                    found = True
                    break
            if not found:
                return None
            
        #True #se a palavra tem que obrigatoriamente ter sido inserida: current_node.is_leaf    
        return current_node if current_node.is_leaf else None
    
    def remove(self, word: str):
        """Remove uma palavra da árvore radix. Retorna True se a remoção foi bem-sucedida."""
        return self._remove(self.root, word)

    def _remove(self, node: radixNode, word: str) -> bool:
        """Função auxiliar recursiva para remover uma palavra da árvore radix."""
        if not word:
            # Se a palavra está vazia, chegamos ao fim da palavra a ser removida
            if node.is_leaf:
                node.is_leaf = False  # Desmarca o nó como folha
                # Verifica se o nó não tem filhos para possivelmente removê-lo
                return len(node.children) == 0  # Retorna True se o nó pode ser removido
            return False  # A palavra não estava presente

        # Percorre os filhos procurando o próximo prefixo
        for key, child in node.children.items():
            common_prefix_len = node._common_prefix_lenght(word, child.prefix)
            if common_prefix_len == len(child.prefix):
                # A parte correspondente do prefixo foi encontrada
                if self._remove(child, word[common_prefix_len:]):
                    # Remove o nó filho se ele estiver vazio e não for uma folha
                    del node.children[key]

                    # Após remover o filho, verifica se o nó atual ainda precisa existir
                    return not node.is_leaf and len(node.children) == 0
                return False
        return False
    
    def print_tree(self):
        def _print_node(node : radixNode, prefix=""):
            # Imprime o prefixo atual e se é uma folha
            is_leaf = f"(folha) => {node.value} " if node.is_leaf else ""
            print(f"{prefix}{node.prefix} {is_leaf} {node.parent.value if node.parent is not None else "NONE"}" )

            # Percorre recursivamente os filhos
            for child in node.children.values():
                _print_node(child, prefix + "  ")

        # Inicia a impressão a partir da raiz
        _print_node(self.root)

    def get_word(self, curNode):
        word = bytearray()
        while curNode and curNode.parent:
            word = curNode.prefix + word
            curNode = curNode.parent
        return word

    def print_inverted_list(self):
        for it, elem in enumerate(self.indexTable):
            if elem is None:
                print(it, ": None") 
            else:
                print(it, ":", self.get_word(elem))

            if it >= self.many_words:
                break