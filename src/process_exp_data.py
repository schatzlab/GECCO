import os

def main():
  """ This script will take the raw expression data table from ICGC
    (exp_seq.tsv) and generate two files proces in the directory "EXP":

    1) exp_seq.cleaned --> A cleaned/reformatted version of the ICGC expression
       data containing only the donor ID, normalize read counts, raw read
       counts, and gene IDs in tab delimited format.

    2) exp_seq.cleaned.filtered --> the expression data based on donors and
       genes. We make sure to ignore (1) any donors that don't have accompanying
       SSM data and (2) any genes that are underrepresented across donors.
  """

  # Create the output directory for all processed expression data.
  if not os.path.exists("EXP"):
      os.makedirs("EXP")

  # Clean the raw expression data and extract basic gene/donor info:
  print("Step 1: Reformatting expression data and computing stats.")
  donor_list, gene_tally  = cleanExpressionData("exp_seq.tsv",
                                                "EXP/exp_seq.cleaned")

  # Find list of genes that are underrepresented across all donors:
  print("Step 2: Identifying underrepresented genes.")
  bad_genes = []
  for gene_id, tally in gene_tally.iteritems():
    if tally < len(donor_list):
      bad_genes.append(gene_id)

  # Find list of donors that don't have accompanying SSM data. Also write
  # The full list of filtered donors to file for later use.
  print("Step 3: Identifying donors that lack both EXP and SSM data")
  donors_with_SSM_data = open("WGS/donor_files_filtered.txt")
  donor_with_all_data = open("donors_with_EXP_and_SSM_data.txt", "w")
  donor_list_filtered = []

  for row in donors_with_SSM_data:
    donor = row.strip().split('.')[0]
    if donor in donor_list:
      donor_list_filtered.append(donor)
      donor_with_all_data.write(donor + '\n')

  donors_with_SSM_data.close()
  donor_with_all_data.close()


  # Filter out expression data that fail the donor and gene requirements.
  print("Step 4: Filtering out EXP data that fail the donor and gene requirements")
  filterExpressionData(donor_list_filtered, bad_genes, "EXP/exp_seq.cleaned",
                       "EXP/exp_seq.cleaned.filtered")


def cleanExpressionData(raw_exp_file, cleaned_exp_file):
  """ This function serves two purposes.

      The first purpose is to clean/reformat the raw ICGC expression data so
      each row contains only the following columns:
      1) Donor ID.
      2) Normalized Read Count.
      3) Raw Read Count.
      4) Gene ID.

      The second purpose is extract and return two basic pieces of aggregate
      information about the expression data for later processing:
      1) The list of donors found in the expression file.
      2) The total number of donors with expression data for each gene.

      Args:
      - raw_exp_file: contains the file path for the raw unprocessed
        ICGC expression sequencing data.
      - cleaned_exp_file: the file path for the output file where we
        will write the cleaned and reformatted ICGC data.
  """
  raw_exp_data_in = open(raw_exp_file, "r")
  cleaned_exp_data_out = open(cleaned_exp_file, "w")

  donor_list = []
  gene_tally = {}

  for index, row in enumerate(raw_exp_data_in):
    # Skip the header.
    if (index == 0):
      continue

    # Notify the user every 1 million lines that are processed.
    if (index % 1000000 == 0):
      print("...Processed %i lines." % index)

    fields = row.strip().split("\t")
    donor_id = fields[0]
    norm_reads = fields[8]
    raw_reads = fields[9]
    gene_id = fields[7]

    # Add newly identified donors to the donor_list.
    if donor_id not in donor_list:
      donor_list.append(donor_id)

    # Count the total number donors with expression data for each gene.
    if gene_id not in gene_tally:
      gene_tally[gene_id] = 1
    else:
      gene_tally[gene_id] += 1

    # Write the cleaned data to file.
    output = "\t".join([donor_id, norm_reads, raw_reads, gene_id]) + "\n"
    cleaned_exp_data_out.write(output)

  # Close the files:
  cleaned_exp_data_out.close()
  cleaned_exp_data_out.close()

  # Return the donor list and gene_tally dictionary:
  return donor_list, gene_tally


def filterExpressionData(donor_list_filtered, bad_genes, cleaned_exp_file,
                         filtered_exp_file):
  """ This function will filter the cleaned expression data so that it contains
      only:
      1) Donors with BOTH expression and SSM data.
      2) Genes whose expression were measured in ALL donors across studies.

      Args:
      - donor list_filtered: the list of donors with both EXP and WGS data.
      - bad_genes: the full list of genes that are underrepresented across donors.
      - cleaned_exp_file: the input file path for the cleaned expression data.
      - filtered_exp_file: the output file path for the filtered expression data.
  """

  cleaned_exp_data_in = open(cleaned_exp_file, "r")
  filtered_exp_data_out = open(filtered_exp_file, "w")

  for index, row in enumerate(cleaned_exp_data_in):
    # Notify the user every 1 million lines that are processed.
    if (index % 250000 == 0 and index != 0):
      print("...Processed %i lines." % index)

    fields = row.strip().split("\t")
    donor_id = fields[0]
    norm_reads = fields[1]
    raw_reads = fields[2]
    gene_id = fields[3]

    if donor_id not in donor_list_filtered or gene_id in bad_genes:
      continue
    else:
      filtered_exp_data_out.write(row)

  # Close the data files when finished.
  cleaned_exp_data_in.close()
  filtered_exp_data_out.close()


if __name__ == '__main__':
  main()