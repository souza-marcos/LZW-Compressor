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