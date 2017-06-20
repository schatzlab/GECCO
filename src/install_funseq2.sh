""" This script will:
    1) Download FunSeq2 (v2.1.2)
    2) Download the funseq2 data context (v2.1.2).
    3) Extract and reformat the ENCODE TFP annotations for later analysis.

    To use this script, you must first set the GECCO_PATH below. Next, cd to
    the directory where you would like to install FunSeq2 and run the
    command: './install_funseq.sh'
"""

export GECCO_PATH=

# Download FunSeq2.
wget http://funseq2.gersteinlab.org/static/download/funseq2.1.2.tar.bz2
tar xvjf funseq2.1.2.tar.bz2
cd funseq2-1.2

# Download data context.
# If the wget process fails for any reason you can download the links manually
# from http://funseq2.gersteinlab.org/data/2.1.2.
wget -rkpN -t 1 -e robots=off http://funseq2.gersteinlab.org/data/2.1.2
mv funseq2.gersteinlab.org/static/data_context2.1.2/ ./data_context
rm -rf funseq2.gersteinlab.org

# Extract all TFPs from the Encode data in bed format.
zcat data_context/ENCODE.annotation.gz | grep TFP | sed 's/TFP.//g' > data_context/ENCODE.annotation.TFP

# Calculate aggregate TFP stats over each TFP class.
python ${GECCO_PATH}/calculate_tfp_stats.py data_context/ENCODE.annotation.TFP data_context/TFP_stats
