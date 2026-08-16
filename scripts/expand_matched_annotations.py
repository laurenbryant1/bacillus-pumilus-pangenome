import os
import csv

base = "."  # current folder (gene_annotations)

# Correct EggNOG column names
eggnog_cols = [
    "query", "seed_ortholog", "evalue", "score", "eggNOG_OGs",
    "max_annot_lvl", "COG_category", "Description", "Preferred_name",
    "GOs", "EC", "KEGG_ko", "KEGG_Pathway", "KEGG_Module",
    "KEGG_Reaction", "KEGG_rclass", "BRITE", "KEGG_TC",
    "CAZy", "BiGG_Reaction", "PFAMs"
]

print("\n=== Expanding annotations in all GCA folders ===\n")

for folder in sorted(os.listdir(base)):
    if not folder.startswith("GCA"):
        continue

    folder_path = os.path.join(base, folder)
    if not os.path.isdir(folder_path):
        continue

    # find matched.tsv file
    input_file = None
    for fname in os.listdir(folder_path):
        if fname.endswith("_matched.tsv"):
            input_file = os.path.join(folder_path, fname)
            break

    if input_file is None:
        print(f"⚠ No matched.tsv found in {folder}")
        continue

    output_file = input_file.replace("_matched.tsv", "_matched_expanded.tsv")

    print(f"➡ Processing {input_file}")

    with open(input_file, newline="") as infile, open(output_file, "w", newline="") as outfile:
        reader = csv.reader(infile, delimiter="\t")
        writer = csv.writer(outfile, delimiter="\t")

        header = next(reader)  # original: geneID, status, annotation

        # Build output header
        expanded_header = ["geneID", "status"] + eggnog_cols
        writer.writerow(expanded_header)

        for row in reader:
            anno = row[2]

            # Safely split annotation using csv handling
            parts = next(csv.reader([anno]))

            # Pad missing fields
            while len(parts) < len(eggnog_cols):
                parts.append("")

            # Trim extra fields
            parts = parts[:len(eggnog_cols)]

            writer.writerow([row[0], row[1]] + parts)

    print(f"   ✓ Output → {output_file}\n")

print("=== All done ===\n")
