counter=0
rm -f ${IN}_mapped

while read row; do
  # Get the full list of donors with mutations in this recurrently mutated TFP.
  echo "$row" | awk -F "\t" '{print $6}' | tr ',' '\n' | grep DO | awk -F "(" '{print $1}' > ${IN}_donors

  # Identify any genes within 2kb of the TFP.
  echo "$row" | awk '{print $1"\t"$2-2000"\t"$3+2000"\t"$1}' > ${IN}_loc
  gene=`bedtools intersect -wo -a ${IN}_loc -b ${GECCO_PATH}/genes_ensembl | awk '{print $8}' | sort -V | uniq -c | sort -rg | awk '{print $2}' | head -1`

  # If a gene was found, append the following four columns to the row:
  # 1) Name of gene flanking the TFP (ENSEMBL gene name)
  # 2) Name of gene flanking the TFP (UCSC gene name)
  # 3) Comma separated list of expression values for the gene in donors WITH
  #    at least one mutation in the TFP.
  # 4) Comma separated list of expression values for the gene in donors WITHOUT
  #    at least one mutation in the TFP.
  if [ `echo $gene | wc -c` -gt 4 ]; then
    echo -e "${row}\t${gene}\t"\
    `grep -w $gene ${GECCO_PATH}/gene_converter  | awk '{print $3}' | sort | uniq -c  | sort -rg | awk '{print $2}' | head -1`"\t"\
    `grep -w $gene ${ICGC_PATH}/EXP/exp_seq.cleaned | grep -F -f ${IN}_donors | awk '{print $2}' | grep -v "E-" | tr '\n' ',' | rev | cut -c 2- | rev`"\t"\
    `grep -w $gene ${ICGC_PATH}/EXP/exp_seq.cleaned | grep -vF -f ${IN}_donors | awk '{print $2}' | grep -v "E-" | tr '\n' ',' | rev | cut -c 2- | rev` >> ${IN}_mapped
  fi

  # Notify the user every 100 TFPs that are processed.
  counter=`expr $counter + 1`
  if [ `expr $counter % 100` -eq 0 ]; then
    break
    echo "Processed $counter"
  fi

done < ${IN}

# Remove temp files.
rm ${IN}_donors
rm ${IN}_loc

# Calculate p-values using expression data.
python ${GECCO_PATH}/calculate_pvalues.py ${IN}_mapped ${IN}_done 100000
