###############################################
# Pan-Genome Analysis
# Purpose:
#   Process OrthoFinder N0.tsv output to classify
#   orthogroups as Core, Accessory, or Unique
#   across Bacillus pumilus genomes.
###############################################

# -----------------------------
# 1. Load Required Packages
# -----------------------------
library(tidyverse)

# -----------------------------
# 2. Load and Inspect Data
# -----------------------------
# Replace the path below with your file location
df <- read.delim("N0.tsv",
                 header = TRUE,
                 sep = "\t",
                 fill = TRUE,
                 stringsAsFactors = FALSE)

# Preview the structure of the data
cat("First 10 column names:\n")
print(colnames(df)[1:10])
cat("\nPreview of first few columns:\n")
print(head(df[, 1:5]))

# -----------------------------
# 3. Data Cleaning
# -----------------------------
# Replace blank cells ("") with NA for consistent counting
df[df == ""] <- NA

# -----------------------------
# 4. Count Presence Across Species
# -----------------------------
# Each column after the first 3 (HOG, OG, Gene.Tree.Parent.Clade)
# represents a species. Count how many species have at least one gene
# in each orthogroup.

df$species_count <- rowSums(!is.na(df[, 4:ncol(df)]))

# Quick summary of counts (preliminary check)
cat("\nSummary of preliminary species counts:\n")
print(summary(df$species_count))

# -----------------------------
# 5. Correct Column Range
# -----------------------------
# Exclude the last column if a new one (e.g., species_count)
# was already added earlier in the session.
df$species_count <- rowSums(!is.na(df[, 4:(ncol(df) - 1)]))

# Check the summary again — Max should equal number of genomes (e.g., 53)
cat("\nCorrected species count summary:\n")
print(summary(df$species_count))

# -----------------------------
# 6. Classify Orthogroups
# -----------------------------
# Define total number of genomes (species)
total_species <- 53  # Adjust if different

# Assign categories based on presence pattern
df$category <- case_when(
  df$species_count == total_species ~ "Core",
  df$species_count == 1 ~ "Unique",
  TRUE ~ "Accessory"
)

# View category counts
cat("\nOrthogroup classification summary:\n")
print(table(df$category))

# -----------------------------
# 7. Validation Checks
# -----------------------------
# Confirm all rows classified
cat("\nValidation: total rows and sum of categories\n")
print(nrow(df))
print(sum(table(df$category)))

# Inspect a few examples from each category
cat("\nExamples of Core orthogroups:\n")
print(df %>% filter(category == "Core") %>% head(3))

cat("\nExamples of Accessory orthogroups:\n")
print(df %>% filter(category == "Accessory") %>% head(3))

cat("\nExamples of Unique orthogroups:\n")
print(df %>% filter(category == "Unique") %>% head(3))

# -----------------------------
# 8. Export Results (optional)
# -----------------------------
# Save annotated table with new columns (species_count, category)
write.table(df,
            "N0_with_core_accessory_unique.tsv",
            sep = "\t",
            quote = FALSE,
            row.names = FALSE)

cat("\n Analysis complete. File saved as 'N0_with_core_accessory_unique.tsv'\n")



#------------
# Strain names 
strain_name_df <- readxl::read_xlsx("Bacilus Pumilus Strain Names.xlsx")
head(strain_name_df[, c(1, 4)])

# 2. Create a mapping (accession → strain)
map <- strain_name_df[, c(1, 4)]
colnames(map) <- c("Accession", "StrainName")

# Genome columns (skip metadata + summary)
genome_cols <- colnames(df)[4:(ncol(df) - 2)]

# Check matches
match_report <- data.frame(Accession = character(),
                           StrainName = character(),
                           MatchedColumn = character(),
                           Status = character(),
                           stringsAsFactors = FALSE)

for (i in 1:nrow(map)) {
  acc <- map$Accession[i]
  name <- map$StrainName[i]
  matching_cols <- grep(acc, genome_cols, value = TRUE)
  
  if (length(matching_cols) > 0) {
    cat(paste0("✅ ", acc, " → ", name, " (", paste(matching_cols, collapse = ", "), ")\n"))
    match_report <- rbind(match_report, data.frame(Accession = acc, StrainName = name,
                                                   MatchedColumn = paste(matching_cols, collapse = ", "),
                                                   Status = "Matched"))
  } else {
    cat(paste0("⚠️  ", acc, " (", name, ")\n"))
    match_report <- rbind(match_report, data.frame(Accession = acc, StrainName = name,
                                                   MatchedColumn = NA, Status = "Not Found"))
  }
}

cat("\nMatched:", sum(match_report$Status == "Matched"),
    "| Not found:", sum(match_report$Status == "Not Found"), "\n")

write.csv(match_report, "orthofinder_strain_match_report.csv", row.names = FALSE)

# Rename after verifying matches
for (i in 1:nrow(map)) {
   acc <- map$Accession[i]
   name <- map$StrainName[i]
   matching_cols <- grep(acc, colnames(df)[4:(ncol(df)-2)], value = TRUE)
   colnames(df)[colnames(df) %in% matching_cols] <- name
}
genome_cols <- colnames(df)[4:(ncol(df)-2)]
 write.table(df, "N0_with_strain_names.tsv", sep = "\t", quote = FALSE, row.names = FALSE)

 #------
 # melt to long format
 df_long <- df %>%
   select(all_of(genome_cols), category) %>%
   pivot_longer(cols = all_of(genome_cols),
                names_to = "Strain",
                values_to = "Gene") %>%
   mutate(present = ifelse(!is.na(Gene), 1, 0))
 
 # count genes per strain by category
 flower_table <- df_long %>%
   group_by(Strain, category) %>%
   summarise(GeneCount = sum(present), .groups = "drop") %>%
   pivot_wider(names_from = category, values_from = GeneCount, values_fill = 0)
 
 # view the table
 flower_table

 summary(flower_table$Unique)
 sum(flower_table$Unique == 0)
 
 
 flower_table %>% 
   filter(Unique > 0) %>%
   arrange(desc(Unique))
 