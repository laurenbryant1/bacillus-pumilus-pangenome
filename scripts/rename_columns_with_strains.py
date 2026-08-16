import pandas as pd

uv = pd.read_csv("UV_category_counts.tsv", sep="\t", dtype=str)
strain = pd.read_csv("strain_names.csv", header=None, dtype=str)

# strain file: col 0 = accession, col 3 = strain name
strain = strain[[0, 3]]
strain.columns = ["Accession", "StrainName"]

# --- Strip version numbers ONLY from strain file ---
# (Keep UV as-is because it already has no versions)
strain["Accession"] = strain["Accession"].str.replace(r"\.\d+$", "", regex=True)

# --- Also strip whitespace just in case ---
strain["Accession"] = strain["Accession"].str.strip()
strain["StrainName"] = strain["StrainName"].str.strip()
uv["Genome"] = uv["Genome"].str.strip()

# --- Merge by prefix match ---
merged = uv.merge(strain, left_on="Genome", right_on="Accession", how="left")

# --- Replace Genome with StrainName ---
merged["Genome"] = merged["StrainName"]

# --- Remove helper columns ---
merged = merged.drop(columns=["Accession", "StrainName"])

# --- Save ---
merged.to_csv("UV_category_counts_with_strains.tsv", sep="\t", index=False)

print("Done — saved UV_category_counts_with_strains.tsv")
