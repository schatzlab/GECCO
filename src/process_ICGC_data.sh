# You must set the following three variables:
# 1) GECCO_PATH --> Full path to GECCO scripts and files.
# 2) FUNSEQ_PATH --> Full path to FunSeq install location.
# 3) ICGC_PATH --> Full path to downloaded ICGC data. Must contain:
#    1) simple_somatic_mutation.open.tsv (SSM data)
#    2) exp_seq.tsv (expression data)

export GECCO_PATH=
export FUN_PATH=
export ICGC_PATH=

# Unzip the tsv files containing the ICGC SSM and expression data.
echo -e "\n*** Unzipping SSM and expression data ***"
cd $ICGC_PATH
gunzip -q exp_seq.tsv.gz simple_somatic_mutation.open.tsv.gz

# Process the ICGC SSMs
echo -e "\n*** Processing SSM data ***"
bash ${GECCO_PATH}/process_SSMs.sh

# Creat FunSeq2 Run file
echo -e "\n *** Creating FunSeq2 run file ***"
cd ${ICGC_PATH}/WGS
echo -e '#!/bin/bash\n' > ${FUN_PATH}/run_funseq2.sh
echo "./funseq2.sh -inf bed -nc -o funseq_results -f" `ls *bed | xargs -I @ echo \`pwd\`/@ | tr '\n' ','` >> ${FUN_PATH}/run_funseq2.sh
echo -e "Your FunSeq2 script 'run_funseq2.sh' has been created in:\n${FUN_PATH}"

# Process the ICGC expression data.
echo -e "\n*** Processing expression data ***"
cd $ICGC_PATH
python ${GECCO_PATH}/process_exp_data.py
