import os
import pandas as pd
import json
import re

# --- Load UV keyword categories ---
with open("uv_keywords.json") as f:
    UV = json.load(f)

# --- Open a simple text debug log ---
log = open("debug_log.txt", "w", encoding="utf-8")


def row_matches_category(desc, keywords):
    if pd.isna(desc):
        return False

    desc = str(desc).lower()

    # --- SKIP RULE: ignore all phage-related proteins ---
    if "phage" in desc:
        return False

    for kw in keywords:
        kw = kw.lower().strip()

        # Multi-word → exact phrase match
        if " " in kw:
            if kw in desc:
                return kw

        # Single word → whole word match
        else:
            pattern = r"\b" + re.escape(kw) + r"\b"
            if re.search(pattern, desc):
                return kw

    return False



results = []

for d in sorted(os.listdir(".")):
    if not d.startswith("GCA_") or not os.path.isdir(d):
        continue

    # Find the matched_expanded file
    tsv_file = None
    for f in os.listdir(d):
        if f.endswith("_matched_expanded.tsv"):
            tsv_file = os.path.join(d, f)
            break

    if tsv_file is None:
        print(f"No matched_expanded file found in {d}")
        log.write(f"No matched_expanded file found in {d}\n")
        continue

    df = pd.read_csv(tsv_file, sep="\t", header=None, dtype=str, low_memory=False)
    desc_col = df.iloc[:, 9]

    row = {"Genome": d}

    for category, keywords in UV.items():
        count = 0

        for desc in desc_col:
            match_kw = row_matches_category(desc, keywords)
            if match_kw:
                count += 1
                # WRITE A SIMPLE DEBUG LINE
                log.write(f"{d} | {category} | matched '{match_kw}' in: {desc}\n")

        row[category] = count

    results.append(row)

# Save counts
out = pd.DataFrame(results)
out.to_csv("UV_category_counts.tsv", sep="\t", index=False)

log.close()

print("Done.")
print("Debug log saved to debug_log.txt")
