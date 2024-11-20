# Testes Realizados

Para testarmos o desempenho e corretude do algoritmo, foram realizados testes de compressão e descompressão em três tipos diferentes de arquivos:

- Arquivos Binários
- Arquivos de Imagem
- Arquivos de Texto

A partir [deste script](https://github.com/souza-marcos/LZW-Compressor/blob/main/main.py) que roda o programa em arquivos de uma pasta, foram armazenadas estatísticas de desempenho, as quais também foram usadas para elaborar os gráficos vistos abaixo. Por estas estatísticas podem ser observadas o tamanho original bem como o tamanho comprimido. Dessa forma, nos arquivos utilizados sempre obtivemos sucesso ao comprimir e descomprimir. Também foram verificados a corretude por meio do comando ```diff```, que também verificou que o algoritmo está funcionando corretamente.

# Estatísticas

No gráfico abaixo podemos verificar as médias das taxas de compressão de cada tipo de arquivo, onde é possível perceber que os arquivos binários, em média, obtiveram as maiores taxas de compressão.

![Não foi possível carregar a imagem](https://github.com/souza-marcos/LZW-Compressor/blob/main/images/grafico_taxas_compressao.png)

Além disso, também podemos visualizar os intervalos de confiança das taxas de compressão no arquivo abaixo.

![Não foi possível carregar a imagem](https://github.com/souza-marcos/LZW-Compressor/blob/main/images/intervalos_taxas_compressao.png)

Por fim, analisando os dados acima. Percebemos que foi possível realizar compressões em todos os arquivos testados, sendo que o tipo de arquivo com maior variação das taxas de compressão é o arquivo de texto.