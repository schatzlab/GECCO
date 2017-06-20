# GECCO: Genomic Enrichment Computational Clustering Operation

The contributions of coding mutations to tumorigenesis are relatively well known; however, little is known about somatic alterations in noncoding DNA. Here we describe GECCO (Genomic Enrichment Computational Clustering Operation) to analyze somatic noncoding alterations in 308 pancreatic ductal adenocarcinomas (PDAs) and identify commonly mutated regulatory regions. We find recurrent noncoding mutations to be enriched in PDA pathways, including axon guidance and cell adhesion, and newly identified processes, including transcription and homeobox genes. We identified mutations in protein binding sites correlating with differential expression of proximal genes and experimentally validated effects of mutations on expression. We developed an expression modulation score that quantifies the strength of gene regulation imposed by each class of regulatory elements, and found the strongest elements were most frequently mutated, suggesting a selective advantage. Our detailed single-cancer analysis of noncoding alterations identifies regulatory mutations as candidates for diagnostic and prognostic markers, and suggests new mechanisms for tumor evolution.

## Citation ## 

**[Recurrent noncoding regulatory mutations in pancreatic ductal adenocarcinoma](https://www.nature.com/ng/journal/v49/n6/full/ng.3861.html)** <br>
Feigin, ME, Garvin, T, Bailey, P, Waddell, N, Chang, DK, Kelley, DR, Shuai, S, Gallinger, S, McPherson, JD, Grimmond, SM, Khurana, E, Stein, LD, Biankin, AV, Schatz, MC, Tuveson, DA (2017) Nature Genetics doi:10.1038/ng.3861

## Running GECCO ##

1. Download GECCO scripts from Github

2. Install FunSeq2 by running the script "install_funseq2.sh". (Note it looks like some of the data_context files have bad URLs on the funseq site so we've reached out for a fix)

3. Download ICGC data.

    1. Go to https://dcc.icgc.org/projects.
    2. Use the toolbar on the left to select any cancer samples of interest.
    3. Click on the 'Details' tab between 'Summary' and 'History'.
    4. In the table click the blue link for the SSM total.
    5. At the top of the page where it says "Available Data Type IS SSM AND PROJECT IN", click on any of the projects whose data you would like to remove from the analysis.
    6. Once you have narrowed the data down to the projects of interest click the "Download Donor Data" link above the table.
    7. Download any files you want but make sure "Simple Somatic Mutation" and "Sequencing-based Gene Expression" are selected.
    8. Click the "Download" button.
    9. Once the tar file has finished downloading, unzip it using the command "tar xvf <filename>"

4. Enter the directory containing your ICGC data and run "process_ICGC_data.sh". Make sure to set the path variables before running.

5. Run FunSeq2 using the script created in your FunSeq2 install directory.

6. Enter the directory containing the results of your FunSeq2 run and run "gecco.sh".

7. Once the qsub jobs have all finished, enter the directory containing the results of your FunSeq2 run and run "calculate_false_discovery.sh".

## Getting Help ## 

Please submit any issues or pull requests using the links above
