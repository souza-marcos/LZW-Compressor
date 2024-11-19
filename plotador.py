import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Caminho dos Arquivos
path_bin = '/home/lucasjunq/Desktop/TPA_ALGII/LZW-Compressor/plots/data/stats_bin.txt'
path_images = '/home/lucasjunq/Desktop/TPA_ALGII/LZW-Compressor/plots/data/stats_images.txt'
path_texto = '/home/lucasjunq/Desktop/TPA_ALGII/LZW-Compressor/plots/data/stats_texto.txt'

# Nome das Colunas
colunms_names = ['isCompressed','lzw.memoryDict','lzw.wordsAdded','totalTime', 'fixed_var', 'limSizeCode', 'originalSize', 'compressedSize', 'compressionRatio']

# Dataframes
df_bin = pd.read_csv(path_bin, header=None, names=colunms_names, sep='\s+')
df_images = pd.read_csv(path_images, header=None, names=colunms_names, sep='\s+')
df_text = pd.read_csv(path_texto, header=None, names=colunms_names, sep='\s+')


# Gráfico com as médias das taxas de compressão por tipo de arquivo
columns = ['Bin','Images','Text']
bin_nozero = df_bin[df_bin['compressionRatio'] != 0]
text_nozero = df_images[df_images['compressionRatio'] != 0]
images_nozero = df_text[df_text['compressionRatio'] != 0]
data = [[bin_nozero['compressionRatio'].mean(),images_nozero['compressionRatio'].mean(),text_nozero['compressionRatio'].mean()]]
comp_ratio = pd.DataFrame(data, columns=columns)
df_long = comp_ratio.melt(var_name='Categoria', value_name='Valor')
# sns.barplot(data=df_long, x='Categoria', y='Valor', palette='Blues')
# plt.title('Médias das taxas de compressão por tipo de arquivo')
# plt.ylabel('Taxa de compressão')
# plt.xlabel('Tipo de arquivo')
# plt.show()
# plt.savefig('grafico_taxas_compressao.png', dpi=300, bbox_inches='tight')

# Boxplot das taxas de compressão por tipo de arquivo
data = [[bin_nozero['compressionRatio'],images_nozero['compressionRatio'],text_nozero['compressionRatio']]]
comp_ratio = pd.DataFrame({
    'Bin': bin_nozero['compressionRatio'],
    'Images': images_nozero['compressionRatio'],
    'Text': text_nozero['compressionRatio']
})
sns.boxplot(data=comp_ratio,palette='Blues')
plt.title('Intervalos das taxas de compressão')
plt.ylabel('Taxa de Compressão')
plt.xlabel('Tipo de Arquvivo')
# plt.show()
plt.savefig('intervalos_taxas_compressao.png', dpi=300, bbox_inches='tight')

# df_bin_sc = df_bin[['limSizeCode','compressionRatio']]
# df_bin_sc['Type'] = 'Bin'
# print(df_bin_sc)

# compressed_data = df_text[df_text['isCompressed'] == 1]
# filter = compressed_data['fixed_var'] == 1
# fixed_comp_data = compressed_data[filter]
# variable_comp_data = compressed_data[~filter]
# # Como temos fixo variavel intercalados e 10 a 15 bits em sequencia


# sns.lineplot(data=fixed_comp_data, x='limSizeCode', y='compressionRatio', hue='name')
# plt.show()
# print(fixed_comp_data)
