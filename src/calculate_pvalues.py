import numpy as np
import sys
import re

fin = open(sys.argv[1], 'r')
fout = open(sys.argv[2], 'w')
perm_count = int(sys.argv[3])

perm_t_score=map(float, [0]*perm_count)

for row in fin:
  fields = row.strip().split('\t')

  # Extract the gene expression values for donors with & without TFP mutations.
  exp_non_mut = map(float, fields[9].strip().split(','))
  try:
    exp_mut = map(float, fields[8].strip().split(','))
  #If there are no patients with mutation data, skip the row.
  except:
    continue

  exp_all = exp_mut + exp_non_mut
  n1 = len(exp_mut)
  n2 = len(exp_non_mut)

  # Calculate the true t-score.
  true_t_score=np.abs( (np.mean(exp_mut)-np.mean(exp_non_mut)) /  np.sqrt((np.var(exp_mut)/n1) + (np.var(exp_non_mut)/n2)) )

  # Permute the data "perm_count" times and recompute the t-score.
  for i in range(perm_count):
    perm_data = np.random.permutation(exp_all)
    perm_t_score[i]=(np.abs((np.mean(perm_data[0:n1]) - np.mean(perm_data[n1:(n2+n1)])) /
                     np.sqrt((np.var(perm_data[0:n1])/n1) +(np.var(perm_data[n1:(n2+n1)])/n2))))

  # Calculate the p-value by calculating the fraction of times a permuted
  # t_score was more extreme than the true t-score
  p_value = float(sum(np.array(perm_t_score) > true_t_score)) / perm_count

  # Append the results to the input and write to a new file.
  fout.write('\t'.join(map(str, fields) + [str(n1), str(np.mean(exp_mut)),
                                           str(np.mean(exp_non_mut)),
                                           str(p_value)]) + '\n')
fout.close()
