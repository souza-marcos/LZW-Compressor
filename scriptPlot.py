import matplotlib.pyplot as plt
import pandas as pd

def parseStatsFile(filename):
    columns = [
        "type",           
        "lzw_memoryDict", 
        "lzw_wordsAdded", 
        "totalTime",      
        "mode",           
        "limSizeCode",    
        "originalSize",   
        "compressedSize", 
        "compressionRatio"
    ]

    data = []
    with open(filename, 'r') as file:
        for line in file:
            values = list(map(float, line.strip().split()))
            data.append(values)

    df = pd.DataFrame(data, columns=columns)
    df["type"] = df["type"].astype(int)
    df["mode"] = df["mode"].astype(int)
    df["limSizeCode"] = df["limSizeCode"].astype(int)
    df["originalSize"] = df["originalSize"].astype(int)
    df["compressedSize"] = df["compressedSize"].astype(int)
    df["lzw_wordsAdded"] = df["lzw_wordsAdded"].astype(int)

    df["type"] = df["type"].map({1: "Compression", 0: "Decompression"})
    df["mode"] = df["mode"].map({1: "Variable", 0: "Fixed"})

    df['sizeCategory'] = pd.cut(df['originalSize'], bins=[0, 1e6, 1e7, float('inf')], 
                                labels=['Small', 'Medium', 'Large'])
    
    dec = df["type"] == "Decompression"
    df.loc[dec, ["originalSize", "compressedSize", "compressionRatio"]] = None
    return df

def plot_results(dataframe):
    
    output_dir = "plots"
    import os
    os.makedirs(output_dir, exist_ok=True)

    # A plot to view the compression ratio for each file size category => Small, Medium, Large
    fig, ax = plt.subplots()
    
    ax.hist(dataframe.loc[dataframe["type"] == "Compression", "compressionRatio"], bins=50, alpha=0.5, label="Compression")

    plt.savefig(f"{output_dir}/compression_ratio_by_size_category.png")
    plt.close()

    
    
if __name__ == "__main__":
    stats_file = "stats.txt"
    stats_df = parseStatsFile(stats_file)
    # print(stats_df)

    plot_results(stats_df)
