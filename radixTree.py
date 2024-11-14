class radixNode:
    def __init__(self, prefix: str = "", is_leaf: bool = False):
        # Prefixo associado a este node
        self.prefix = prefix

        # Flag que sinaliza se existe o node é uma folha
        self.is_leaf = is_leaf

        # Dicionário que mapeia nodes filhos de acordo com o primeiro caracter dos prefixos
        self.children: dict[str, radixNode] = {}
    
    def _common_prefix_lenght(self, str1, str2):
        lenght = 0
        max_lenght = min(len(str1),len(str2))
        for i in range(max_lenght):
            if str1[i] != str2[i]:
                break
            lenght = lenght + 1
        return lenght

class radixTree:
    def __init__(self):
        # Raiz da árvore
        self.root = radixNode()
        
        # Quantidade de palavras inseridas na árvore
        self.many_words = 0

    def insert(self, word):
        """Insere uma palavra na árvore radix"""
        current_node = self.root
        # Verificando prefixos em comum entre os filhos
        while word:
            if not current_node.children:
                current_node.children[word[0]] = radixNode(word, True)
                return

            for key, child in current_node.children.items():
                common_prefix_length = current_node._common_prefix_lenght(word, child.prefix)
                
                # Caso exista um filho com prefixo em comum
                if common_prefix_length > 0:
                    # Se o prefixo do node filho precisa ser dividido
                    if common_prefix_length < len(child.prefix):
                        # O node filho é divido
                        split_node = radixNode(child.prefix[common_prefix_length:])
                        split_node.children = child.children
                        split_node.is_leaf = child.is_leaf

                        # Node filho é atualizado
                        child.prefix = child.prefix[:common_prefix_length]
                        child.children = {split_node.prefix[0] : split_node}
                        child.is_leaf = False
                    
                    # Continua o processo com o resto do prefixo de 'word' no nó filho
                    word = word[common_prefix_length:]
                    current_node = child
                    break
            # Caso nenhum prefixo em comum seja encontrado: adiciona novo filho
            else:
                current_node.children[word[0]] = radixNode(word, True)
                return
        current_node.is_leaf = True
    
    def search(self, word):
        """Busca uma palavra na árvore radix"""
        current_node = self.root
        while word:
            found = False
            for key, child in current_node.children.items():
                common_prefix_len = current_node._common_prefix_lenght(word, child.prefix)
                if common_prefix_len > 0:
                    word = word[common_prefix_len:]
                    current_node = child
                    found = True
                    break
            if not found:
                return False
        return current_node.is_leaf #True #se a palavra tem que obrigatoriamente ter sido inserida: current_node.is_leaf
    
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
        def _print_node(node, prefix=""):
            # Imprime o prefixo atual e se é uma folha
            is_leaf = "(folha)" if node.is_leaf else ""
            print(f"{prefix}{node.prefix} {is_leaf}")

            # Percorre recursivamente os filhos
            for child in node.children.values():
                _print_node(child, prefix + "  ")

        # Inicia a impressão a partir da raiz
        _print_node(self.root)