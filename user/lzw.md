# Algoritmo LZW

O algoritmo Lempel-Ziv-Welch (LZW) é um método de compressão de dados sem perdas. O algoritmo foi desenvolvido por Abraham Lempel, Jacob Ziv e Terry Welch em 1984 e é amplamente utilizado em diversos sistemas de compressão de arquivos, um exemplo é o uso de uma variante no sistema de imagens GIF.

## Como funciona

O algoritmo LZW percorre a entrada de dados e tenta encontrar padrões repetidos. Quando um padrão é encontrado, o algoritmo substitui o padrão por um código que o representa. Neste caso, podemos ter códigos de tamanho variável ou fixo, códigos de tamanho variável começam com tamanho 9bits e aumentam de tamanho quando todos os códigos de 9 bits forem utilizados. O algoritmo mantém um dicionário de padrões para códigos, aqui implementados por uma trie compacta.


## Implementação

Como já dito antes, a implementação do algoritmo necessita de um dicionário de padrões para códigos, neste caso como é a proposta do trabalho foi implementado uma árvore radix (árvore Trie de prefixos compacta) para servir como dicionário. Detalhes sobre a implementação da árvore radix podem ser encontrados [aqui](https://github.com/souza-marcos/LZW-Compressor/blob/main/user/radixTree.md)

A principal referência utilizada para a implementação do algoritmo foi [essa aqui](https://www.cs.cmu.edu/~cil/lzw.and.gif.txt), mas também foi utilizado as notas de aula da classe MIT 6.02, que pode ser encontrada [aqui](https://web.mit.edu/6.02/www/s2012/handouts/3.pdf).

Em síntese, o algoritmo LZW funciona da seguinte forma:
### Compressão:
Começamos com o dicionário com todos os bytes possíveis para um caracter (0-255). Percorremos a entrada de dados e tentamos encontrar o maior padrão que já está no dicionário. Quando um padrão não está no dicionário, adicionamos ele e emitimos o código do padrão anterior. O algoritmo termina quando não há mais dados para serem lidos. 

Um detalhe importante é quando a trie atinge o limite de códigos para o tamanho do código atual, neste caso podemos ter duas situações:

1. **Aumentar o tamanho do código**. Aqui acontece apenas no caso variável, onde o tamanho do código aumenta em 1 bit e é emitido o código 2^(qtd bits) - 1 => Sinal de controle que indica ao descompressor que os códigos terão um bit a mais a partir dali.

2. **Limpar a trie e recomeçar a compressão**. Aqui acontece no caso fixo ou quando o limite de bits definido pelo usuário é atingido no caso de códigos de tamanho variável.  Neste caso, a trie é reinicializada e a compressão continua.

### Descompressão: 
Começamos com o dicionário com todos os bytes possíveis (0-255). Percorremos a entrada de dados e tentamos encontrar o código no dicionário. Para isso utilizamos uma lista invertida definida no dicionário, que mapeia os códigos para os nós da árvore, que percorrendo os nós pais até a raiz pode-se encontrar a cadeia correspondente ao código. 
    
Quando um código não está no dicionário, adicionamos ele e emitimos a cadeia correspondente ao código anterior (por meio do método descrito anteriormente). O algoritmo termina quando não há mais dados para serem lidos. Observe que são fundamentais os códigos de controle, que indicam ao descompressor que os códigos terão um bit a mais a partir dali.

## Detalhes

A implementação pode ser encontrada [neste arquivo](https://github.com/souza-marcos/LZW-Compressor/lzw.md)