""" Takes as input a raw ICGC SSM file (simple_somatic_mutation.open.tsv) and
    outputs the mutations for EACH donor in a SEPARATE bed file in the proper
    format to be input to the FunSeq2 pipeline:
    1) Chromosome.
    2) Chromosome start position.
    3) Chromosome end position.
    4) Reference allele.
    5) Alternative allele.

    To use this script run the command: "python process_SSMs.py"

    WARNING: This script works given the current format of ICGC ssm.tsv files.
    If ICGC changes the columns/formatting this script will no longer work
    correctly. Below the code is a final comment block that contains the column
    numbers and contents at the time this code was written.
"""
exp_data = open("simple_somatic_mutation.open.tsv", 'r')
line_counter = 0
file_dict = {}

for line in exp_data:
  # Notify the user every 1 million lines that are processed.
  line_counter +=1
  if (line_counter % 1000000 == 0):
    print("...Processed %i SSMs." % line_counter)

  # Extract the necessary fields for FunSeq2.
  fields = line.strip().split("\t")
  donor_id = fields[1]
  chrom = "chr" + fields[8]
  start = fields[9]
  end = fields[10]
  ref_allele = fields[15]
  alt_allele = fields[16]

  # Skip any SSMs that weren't found using WGS (i.e. they were instead WXS, etc).
  sequencing_type = fields[33]
  if sequencing_type != 'WGS':
    continue

  # Open a new <donor_id>.bed file for writing if one has not yet been created.
  if donor_id not in file_dict:
    output_file = open("WGS/" + donor_id + ".bed", "w")
    file_dict[donor_id] = output_file

  # Write each SSM to the proper donor file.
  output_file = file_dict[donor_id]
  output_string = "\t".join([chrom, start, end, ref_allele,alt_allele]) + "\n"
  output_file.write(output_string)

# Close each of the output donor files.
for donor_id, output_file in file_dict.iteritems():
  output_file.close()


""" Column contents for simple_somatic_mutation.open.tsv:
    (0, 'icgc_mutation_id')
    (1, 'icgc_donor_id')
    (2, 'project_code')
    (3, 'icgc_specimen_id')
    (4, 'icgc_sample_id')
    (5, 'matched_icgc_sample_id')
    (6, 'submitted_sample_id')
    (7, 'submitted_matched_sample_id')
    (8, 'chromosome')
    (9, 'chromosome_start')
    (10, 'chromosome_end')
    (11, 'chromosome_strand')
    (12, 'assembly_version')
    (13, 'mutation_type')
    (14, 'reference_genome_allele')
    (15, 'mutated_from_allele')
    (16, 'mutated_to_allele')
    (17, 'quality_score')
    (18, 'probability')
    (19, 'total_read_count')
    (20, 'mutant_allele_read_count')
    (21, 'verification_status')
    (22, 'verification_platform')
    (23, 'biological_validation_status')
    (24, 'biological_validation_platform')
    (25, 'consequence_type')
    (26, 'aa_mutation')
    (27, 'cds_mutation')
    (28, 'gene_affected')
    (29, 'transcript_affected')
    (30, 'gene_build_version')
    (31, 'platform')
    (32, 'experimental_protocol')
    (33, 'sequencing_strategy')
    (34, 'base_calling_algorithm')
    (35, 'alignment_algorithm')
    (36, 'variation_calling_algorithm')
    (37, 'other_analysis_algorithm')
    (38, 'seq_coverage')
    (39, 'raw_data_repository')
    (40, 'raw_data_accession')
    (41, 'initial_data_release_date')
"""