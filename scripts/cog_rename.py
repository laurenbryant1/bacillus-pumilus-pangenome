import pandas as pd
import re

# -------------------------------------------------
# Load strain table (with real headers)
# -------------------------------------------------
df = pd.read_csv("strain_names.csv", dtype=str)

ACC_COL = "Assembly Accession"
STRAIN_COL = "Organism Infraspecific Names Strain"

def clean_acc(acc):
    """
    Remove version (.1/.2) because COG/OrthoFinder outputs often drop it.
    """
    if pd.isna(acc):
        return ""
    acc = str(acc).strip()
    return acc.split(".")[0]   # keep only GCA_#########

# -------------------------------------------------
# Build mapping: accession → strain name
# -------------------------------------------------
mapping = {}

for _, row in df.iterrows():
    acc_raw = row[ACC_COL]
    strain_raw = row[STRAIN_COL]

    if pd.isna(acc_raw) or pd.isna(strain_raw):
        continue

    acc_clean = clean_acc(acc_raw)
    strain_clean = strain_raw.strip()

    mapping[acc_clean] = strain_clean

print(f"Loaded {len(mapping)} strain mappings")

# -------------------------------------------------
# Load your Newick tree
# -------------------------------------------------
with open("Orthofinder_species_tree.newick", "r") as f:
    tree = f.read()

# -------------------------------------------------
# Replace accession names in the tree
# -------------------------------------------------
for acc, strain in mapping.items():
    # match accession with optional version (.1) and optional suffix (_ASMXXXX)
    pattern = rf"{acc}(?:\.\d+)?(?:_[A-Za-z0-9\.]+)?"
    tree = re.sub(pattern, strain, tree)

# -------------------------------------------------
# Save updated tree
# -------------------------------------------------
with open("Orthofinder_species_tree.newick", "w") as f:
    f.write(tree)

print("Renaming complete → Orthofinder_species_tree_renamed.newick")
