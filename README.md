# *Bacillus pumilus* pan-genome and UV-related functions

Comparative genomics of 53 *B. pumilus* genomes.

1. Characterize accessory and unique orthogroups in *B. pumilus* strains
2. Quantify UV-related functions in those orthogroups

## Pipeline

- Mine NCBI for *B. pumilus* genomes
- Keep chromosome and complete assemblies with >30× coverage
- Annotate 53 genomes with Prokka
- Infer orthogroups with OrthoFinder on the [Galaxy](https://usegalaxy.org/) web server; classify core / accessory / unique
- Annotate accessory and unique orthogroups with [eggNOG-mapper](http://eggnog-mapper.embl.de/) online (COG, KEGG, PFAM, descriptions)
- Count UV-resistance keywords from eggNOG functional annotations

OrthoFinder was run on Galaxy (Galaxy Version 2.5.5+galaxy1) to find orthogroups in the set of proteomes.

Functional annotation was performed with eggNOG-mapper v3.0.0 (Cantalapiedra et al., 2021) using orthology assignments from the eggNOG 7 database (Hernández-Plaza et al., 2026). Homology searches used DIAMOND in sensitive mode (e-value ≤ 0.001), transferring GO, KEGG, COG and PFAM terms from orthologs within the automatically adjusted taxonomic scope (`--tax_scope auto`).

Raw genomes, Prokka outputs, full OrthoFinder tables, and eggNOG dumps are omitted because of size. They can be regenerated from the public NCBI accessions in [`config/strain_names.csv`](config/strain_names.csv).

## Repository contents

| Path | Contents |
|------|----------|
| [`config/strain_names.csv`](config/strain_names.csv) | NCBI assembly accessions and strain names (53 genomes) |
| [`config/uv_keywords.json`](config/uv_keywords.json) | Keyword lists for DNA repair, ROS detox, spore, pigment, and protein quality control |
| [`scripts/`](scripts/) | Analysis code used for pan-genome classification, annotation expansion, COG matrices, and UV counts |
| [`results/pangenome/N0_with_core_accessory_unique.tsv`](results/pangenome/N0_with_core_accessory_unique.tsv) | Orthogroups labeled core / accessory / unique |
| [`results/pangenome/accessory_core.tsv`](results/pangenome/accessory_core.tsv) | Per-strain accessory and unique counts |
| [`results/pangenome/Unique_Orthogroups.tsv`](results/pangenome/Unique_Orthogroups.tsv) | Strain-specific orthogroups |
| [`results/functional/UV_category_counts_with_strains.tsv`](results/functional/UV_category_counts_with_strains.tsv) | UV-related category counts by strain |
| [`results/functional/COG_matrix_strain_names.tsv`](results/functional/COG_matrix_strain_names.tsv) | COG category counts across genomes |
| [`results/trees/species_tree.png`](results/trees/species_tree.png) | OrthoFinder species tree |
| [`Bryant_Lauren_Bpumilus_pangenome_Presentation.pdf`](Bryant_Lauren_Bpumilus_pangenome_Presentation.pdf) | Project presentation |

Scripts were run in the original working directory layout and need those large intermediates to re-execute end-to-end. They are included here as the analysis code, not as a standalone pipeline.

## Software

- Python 3 with `pandas` (`scripts/*.py`)
- R with `tidyverse` and `readxl` (`scripts/pan_genome_analysis.R`)
- Prokka (genome annotation)
- OrthoFinder 2.5.5+galaxy1, run on the Galaxy web server
- eggNOG-mapper v3.0.0 (eggNOG 7), run on the eggNOG-mapper website
