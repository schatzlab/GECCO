# You must set the following three variables:
# 1) GECCO_PATH --> Full path to GECCO scripts and files.
# 2) FUNSEQ_PATH --> Full path to FunSeq install location.
# 3) ICGC_PATH --> Full path to downloaded ICGC data. Must contain:
#    1) simple_somatic_mutation.open.tsv (SSM data)
#    2) exp_seq.tsv (expression data)

export GECCO_PATH=
export FUN_PATH=
export ICGC_PATH=

# Clean the top directory by moving all of the generated FunSeq2 VCF files
# into their own directory.
mkdir -p vcfs
mv *.vcf vcfs

# Extract TFP elements from Recur.Summary and reformat to bed format where
# each line contains a single TFP element. The output will be in
# Recur.Summary.TFP.bed of the format:
# 1) Chromosome.
# 2) Start position.
# 3) End position.
# 4) TFP Class.
# 5) % of patients with at least 1 non-coding mutation in the TFP element.
# 6) Comma separated list of patients and the exact coordinates of any
#    mutations found in the TFP element.
grep TFP Recur.Summary | awk -F "\t" '{print $1}' | tr '()|:-' '\t' | awk '{print $3"\t"$4"\t"$5"\t"$2}' > temp1
grep TFP Recur.Summary | awk -F "\t" '{print $2}' | tr '()' '\t' | awk -F "\t" '{print $2}' > temp2
grep TFP Recur.Summary | awk -F "\t" '{print $3}' > temp3
paste temp1 temp2 temp3 > Recur.Summary.TFP.bed
rm temp1 temp2 temp3

# Calculate the mutation rates for each TFP class given the SSM data. Outputs
# a file, TFP_mutation_rates, with the format:
# 1) TFP Class.
# 2) Number of TFP elements with mutations in at least 1 patient.
# 3) Total number of TFP elements across the genome.
# 4) Fraction of TFP elements with mutations in at least 1 patient.
awk '{print $4}' Recur.Summary.TFP.bed | sort | uniq -c | awk '{print $2"\t"$1}' > temp

while read line; do
  grep -w `echo $line | awk '{print $1}'` ${FUN_PATH}/data_context/TFP_stats
done < temp | awk '{print $2}' > temp2

paste temp temp2 | awk '{print $1"\t"$2"\t"$3"\t"100*$2/$3}' | sort -k4,4rg > TFP_mutation_rates_test
rm temp temp2

# Split the Summary file into 256 separate files for parallel processing.
mkdir split_files
cnt=$((1+`wc -l < Recur.Summary.TFP.bed`/256))
split -d -a 3 -l $cnt Recur.Summary.TFP.bed split_
mv split_[0-9]* split_files
cd split_files

# For each recurrently mutated TFP:
# 1) Associate each TFP with the closest gene within 2kb.
# 2) Find the expression level of that gene for each donor.
# 3) Map gene names from ENSEMBL to UCSC.
# 4) Calculate differential expression and generate p-value.
for i in {000..255}; do
  qsub -cwd -l m_mem_free=1G -v IN=split_${i} -v GECCO_PATH=$GECCO_PATH \
  -v ICGC_PATH=$ICGC_PATH ${GECCO_PATH}/calculate_pvalues.sh
done
