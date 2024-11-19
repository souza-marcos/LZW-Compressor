# A Árvore de Prefixos (Trie)

A árvore de prefixos, também conhecida como Trie, é uma estrutura de dados utilizadas para, dado um certo alfabeto, armazenar chaves (geralmente cadeias de caracteres) em um conjunto. Seu inventor, Edward Fredkin, batisou esta estrutura como Trie com inspiração no termo 'Re**tri**eval' do inglês, pois estas árvores são utilizadas exatamente para a recuperação de dados. Este tipo de estrutura também possui utilidades em diversas tarefas, como:

- Localizar palavras em documentos
- Mineração de Dados
- Implementação de corretores ortográficos
- Realizar casamentos de padrões

As árvores de prefixo possuem uma estrutura em que o a posição de um nó na árvore define a chave ao qual este nó está associado, desse modo o valor de cada nó é destribuído através da estrutura. A raiz dessa árvore geralmente é vazia e todos os filhos de um nó possuem um prefixo em comum com a string associada ao nó pai. Além disso, não são associados valores a todos os nós, sendo que apenas as folhas e alguns nós internos da árvore possuem valores associados.

A complexidade das operações de inserção, remoção e busca de cadeias de caracteres na árvore de prefixos é linear.

![Não foi possível carregar a imagem](https://github.com/souza-marcos/LZW-Compressor/blob/main/images/Trie.jpg)

# A Árvore de Prefixos Compacta (Árvore Radix)

A árvore radix é nada mais é que uma árvore Trie com complexidade espacial otimizada, isto é, uma Trie compactada para diminuir o custo de armazenamento. A árvore radix é construída de modo que nós com apenas um filho são condensados nos nós pais.

![Não foi possível carregar a imagem](https://github.com/souza-marcos/LZW-Compressor/blob/main/images/Radix.jpg)

# Implementação

A estrutura da árvore implementada é muito simples, cada nó da árvore, com exceção da raiz, armazena um prefixo e contém um map para armazenar os nós filhos, sendo que, este map mapeia cada nó filho ao primeiro caracter do prefixo que ele armazena.

# Inserção

Para realizar uma inserção na árvore, percorremos a árvore de modo iterativo. Caso a árvore esteja vazia, adicionamos um nó filho cujo o prefixo é a palavra a ser inserida, caso não seja encontrado um filho com prefixo um comum, criamos um nó filho novo, que contém o este prefixo. Além disso, caso seja encontrado um nó filho que contenha um prefixo em comum, duas situações podem ocorrer:
1. O prefixo em comum é menor que o prefixo do nó filho: Neste caso o nó filho é dividido e um novo ramo é criado.
2. O prefixo em comum é igual o prefixo do nó filho: Neste caso, o nó filho é marcado com um valor associado a uma chave.

# Busca

Para realizar uma busca na árvore percorremos a árvore iterativamente, de modo a acumular prefixos. Caso a palavra a ser encontrada tenha sido inteiramente formada pelo acumúlo dos prefixos, retornamos que a palavra foi encontrada. Caso seja alcançada uma folha e a palavra não tenha sido formada completamente, ou não haja mais nós filhos com prefixos em comum, retornamos que a palavra não foi encontrada.

# Remoção

Para realizar a remoção de uma palavra na árvore, fazemos um caminhamento enquanto acumulamos prefixos a cada nó visitado. Caso alcancemos um nó folha e a palavra a ser removida não tenha sido completamente formada pelos acúmulos dos prefixos, retoramos que a palavra não estava presente na árvore. Caso a palavra a ser removida tenha sido encontrada, realizamos duas operações:
1. Caso o nó seja uma folha, ele é removido.
2. Caso o nó pai tenha apenas um filho, este filho é condensado no nó pai.