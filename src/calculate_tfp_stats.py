""" Takes as input a bed format list of encode TFP elements and outputs a
    4-column tab delimited file for each TFP class with the following stats:
    1) TFP class name.
    2) TFP count (number of TFP elements of the given class in the genome).
    3) TFP total sequence length (total number of bases spanned by all elements of this TFP class).
    4) TFP mean sequence length (mean length of elements of this class across the genome).
"""
import sys

encode_tfp_annotations = open(sys.argv[1], 'r')
tfp_class_stats = open(sys.argv[2], 'w')

TFP_dict = {}
for line in encode_tfp_annotations:
  fields = line.strip().split()
  TFP_length = int(fields[2]) - int(fields[1])
  TFP_class = fields[3]

  # For each element of a given TFP class, tally the total count + cumulative length.
  if TFP_class not in TFP_dict:
    TFP_dict[TFP_class] = [1, TFP_length]
  else:
    TFP_dict[TFP_class][0] += 1
    TFP_dict[TFP_class][1] += TFP_length

# Save the stats for each class to file.
for TFP_class, TFP_info in TFP_dict.iteritems():
  TFP_count = TFP_info[0]
  TFP_cumulative_length = TFP_info[1]
  TFP_mean_length = round(float(TFP_cumulative_length) / TFP_count, 2)
  output_string = '\t'.join([TFP_class, str(TFP_count), str(TFP_cumulative_length),
                            str(TFP_mean_length)]) + '\n'
  tfp_class_stats.write(output_string)

# Close the file.
tfp_class_stats.close()
