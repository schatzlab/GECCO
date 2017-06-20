# Extract all SSMs identified through WGS and save them into a donor specific
# bed file in the proper format to be input to FunSeq2.
echo -e "Step 1: Cleaning and reformatting SSM data."
mkdir -p WGS
python ${GECCO_PATH}/process_SSMs.py

# Sort the donor bed files and uniq any duplicate SSMs (many identical
# variants will be listed multiple times).
echo -e "Step 2: Sorting donor SSM files and removing duplicates."
cd WGS
ls *.bed > donor_files_all.txt
while read donor_file; do
  sort $donor_file | uniq > temp
  mv temp $donor_file
done < donor_files_all.txt

# Ignore files with less than 100 variants (these are likely errors).
echo -e "Step 3: Filter out donor files with abnormally low SSM counts."
mkdir -p low
wc -l *bed | grep -v total | awk '{if ($1 <100) print $2}' > donor_files_low.txt
while read donor_file; do
  mv $donor_file low;
done < donor_files_low.txt

# We choose to ignore donors with SSM counts more than 3 standard deviations
# from the mean. These donors may have chromosome instability and mutations in
# DNA repair proteins putting them into a separate subclass of donors.
echo -e  "Step 4: Filter out donor files with abnormally high SSM counts."
mkdir -p high
STD_DEV=`wc -l *.bed | grep -v total | awk '{SUM+=$1; SUMSQ+=$1**2} END {print sqrt(SUMSQ/NR - (SUM/NR)**2)}'`
wc -l *.bed | grep -v total | awk -v STD_DEV=$STD_DEV '{if ($1 > (3*STD_DEV)) print $2}' > donor_files_high.txt
while read donor_file; do
  mv $donor_file high;
done < donor_files_high.txt

# Create a list of all donor files that passed filtering.
ls *.bed > donor_files_filtered.txt

echo -e "Finished!"
