import os
import pandas as pd

# COG descriptions
COG_DESC = {
    "J": "Translation, ribosomal structure and biogenesis",
    "A": "RNA processing and modification",
    "K": "Transcription",
    "L": "Replication, recombination and repair",
    "B": "Chromatin structure and dynamics",

    "D": "Cell cycle control, cell division, chromosome partitioning",
    "Y": "Nuclear structure",
    "V": "Defense mechanisms",
    "T": "Signal transduction mechanisms",
    "M": "Cell wall/membrane/envelope biogenesis",
    "N": "Cell motility",
    "Z": "Cytoskeleton",
    "W": "Extracellular structures",
    "U": "Intracellular trafficking, secretion, vesicular transport",
    "O": "Posttranslational modification, protein turnover, chaperones",

    "C": "Energy production and conversion",
    "G": "Carbohydrate transport and metabolism",
    "E": "Amino acid transport and metabolism",
    "F": "Nucleotide transport and metabolism",
    "H": "Coenzyme transport and metabolism",
    "I": "Lipid transport and metabolism",
    "P": "Inorganic ion transport and metabolism",
    "Q": "Secondary metabolites biosynthesis, transport, catabolism",

    "R": "General function prediction only",
    "S": "Function unknown",
}

# fixed order of letters
COG_ORDER = list(COG_DESC.keys())

dfs = []

for folder in os.listdir("."):
    if folder.startswith("GCA_"):
        file = os.path.join(folder, "COG_counts.tsv")
        if not os.path.exists(file):
            continue

        df = pd.read_csv(file, sep="\t")
        df = df.set_index("COG")
        df = df.reindex(COG_ORDER).fillna(0).astype(int)
        df = df.rename(columns={df.columns[0]: folder})

        dfs.append(df)

# Merge all genomes
merged = pd.concat(dfs, axis=1)

# Add descriptions
merged.insert(0, "Description", [COG_DESC[c] for c in merged.index])

# Save
merged.to_csv("COG_matrix_with_descriptions.tsv", sep="\t")

print("Saved merged matrix with descriptions: COG_matrix_with_descriptions.tsv")
