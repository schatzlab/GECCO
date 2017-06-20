# Calculate stats for ALL variants.
cd ${GECCO_PATH}
cat split_files/*_done > Recur.Summary.TFP.processed

# Calculate qvalues for variants with expression data in at least 3 patients.
cutoff=3
awk -F "\t" -v cutoff=$cutoff '{if ($11 >= cutoff) print $0}' Recur.Summary.TFP.processed > temp
awk -F "\t" '{print $14}' temp > pvalues.txt

Rscript calculate_false_discovery.R
tail -n +4 qvalue_report.txt > qvalues.txt
rm qvalue_report.txt

paste qvalues.txt temp | sort -k1,1g -k2,2g | awk '{if ($1 > 0) print $0}' > Recur.Summary.TFP.processed_${cutoff}
rm temp