## Instruções de uso do programa principal

### Formato do comando

```bash
python3  main.py [-h] --mode {compress,decompress} [--stats] [--variant {fixed,variable}] [--maxbits MAXBITS] input output
```

### Significado dos argumentos

- **Argumentos obrigatórios**:
    - _input_: Arquivo de entrada para compressão/descompressão em formato não comprimido
    - _output_: Arquivo de saída para compressão/descompressão 

    - _--mode {compress,decompress}_: Modo de operação: compressão ou descompressão

- **Argumentos opcionais**:
    - _-h, --help_: Mostra a mensagem de ajuda e sai
    - _--stats_: Salvar estatísticas no arquivo stats.txt
    - _--variant {fixed,variable}_: Código do compressão deve ser fixo ou variável. Por padrão é fixo.
    - _--maxbits MAXBITS_: Número máximo de bits para o código de compressão, deve ser maior que 8. Caso não seja informado, terá tamanho 12.


### Exemplos de uso
```bash
python3 main.py --mode compress --stats inputs/test.txt  outputs/compressed/test.lzw --maxbits 15 --variant variable
``` 

```bash
python3 main.py --mode decompress --stats outputs/compressed/test.lzw outputs/decompressed/test.txt --maxbits 15 --variant variable
``` 


**Nota**: O arquivo de entrada deve ser um arquivo de texto não comprimido. O arquivo de saída será um arquivo comprimido no formato .lzw. Para descomprimir, o arquivo de entrada deve ser um arquivo comprimido no formato .lzw e deve ser usado os mesmos argumentos de limite de bits e tamanho fixo ou variável, utilizados na compressão.


## Script para acumular estatísticas de vários testes
- Arquivo ```scriptRunAll.sh```
### Formato do comando

```bash
./scriptRunAll.sh
```
Necessário dar permissão de execução ao script com o comando ```chmod +x scriptRunAll.sh```.


## Programa para gerar plots de estatísticas
- Arquivo ```scriptPlot.py```
### Formato do comando

```bash
python3 scriptPlot.py
```