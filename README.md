# Synthesis_Three_Years_Bernburg
[![code](https://img.shields.io/badge/code%20DOI-10.5281%2Fzenodo.17794467-blue)](https://doi.org/10.5281/zenodo.17794467)
[![dataset](https://img.shields.io/badge/dataset%20DOI-10.20387%2Fbonares--w669--gdsd-green)](https://doi.org/10.20387/bonares-w669-gdsd)

The repository contains our amplicon and follow-up analysis from the three years synthesis that we performed from different studies conducted in Bernburg, 
which is a follow up publication from our previous study:

["Two decades long-term field trial data on fertilization, tillage, and crop rotation focusing on soil microbes"](https://doi.org/10.1038/s41597-025-05314-z).

Usually, cultivator tillage shows higher soil organic matter content than mouldboard-plough tillage, but it is unclear how it is connected to the microbial activity. 
The present study addresses this by showing that cultivator tillage has a higher compositional ratio of _K_- to _r_-strategist bacterial taxa than mouldboard-plough tillage 
in the bulk soil, but not in the rhizosphere.
## Folder Structure 
### Preparation
Python scripts to prepare the dataset from the BonaRes Repositroy ["Westerfeld: Long-term field trial on tillage and fertilization in crop rotation"](https://doi.org/10.20387/bonares-w669-gdsd)
can be accessed [`here`](Preparation). The scripts generate tables for the folder [`InputData`](InputData) or provide details used within the manuscript. 
### 16S_ASVdada2
This folder contains the proscessing of the 16S rRNA gene amplicon sequencing data. The data can be downloaded via the ascension numbers (Table S1) using SRA toolkit, with the prefetch and fasterq-dump functions. 
### InputData
This folder includes files are required to execute the R code.
### Fig1_SoilLab
The R code and the plot for Figure 1 can be accessed [`here`](Fig1_SoilLab). The R code saves Table S2 in the folder [`OutputData`](OutputData). 
### Fig2_ResponderPlot
The R code and the plot for Figure 2 can be accessed [`here`](Fig2_ResponderPlot). The R code saves Table S3 in the folder [`OutputData`](OutputData). 
### Fig3_LinearRegression
The R code and the plot for Figure 3 can be accessed [`here`](Fig3_LinearRegression).
### Fig4_growth_rates_plot
The R code and the plot for Figure 4 can be accessed [`here`](Fig4_growth_rates_plot). The R code saves Table S4 in the folder [`OutputData`](OutputData). 
### Fig5_Phylum
The R code and the plot for Figure 5 can be accessed [`here`](Fig5_Phylum).
### Fig6_ASV_Ratios
The R code and the plot for Figure 6 can be accessed [`here`](Fig6_ASV_Ratios).
### OutputData
Tables S2-S4 can be accessed [`here`](OutputData). 
### FigS1_QQPlot
The plot for Figure S1 can be accessed [`here`](FigS1_QQPlot). This plot is generated using the code from Figure 1.
### FigS2_SoilData
The python code, the raw data from 2009 and the plot for Figure S2 can be accessed [`here`](FigS2_SoilData).
### FigS3_rarecurve
The R code and the plot for Figure S3 can be accessed [`here`](FigS3_rarecurve).
### FigS4_Distribution_Plots_ASV_Ratios
The Figure S4 can be accessed [`here`](FigS4_Distribution_Plots_ASV_Ratios). This plot is generated using the code from Figure 6.
### FigS5_permanovaplots
The Figure S5 can be accessed [`here`](FigS5_permanovaplots). This plot is generated using the code from Figure 2.
### FigS6_VennDiagrams
The Figure S6 can be accessed [`here`](FigS6_VennDiagramms). This plot is generated using the code from Figure 2.
### FigS7_VennDiagrams
The Figure S7 can be accessed [`here`](FigS7_VennDiagramms). This plot is generated using the code from Figure 2.
### FigS8_unimodal
The Figure S8 can be accessed [`here`](FigS8_unimodal). This plot is generated using the code from Figure 6.
### FigS9_Genome_size_ASV_Ratios
The Figure S9 can be accessed [`here`](FigS9_Genome_size_ASV_Ratios). This plot is generated using the code from Figure 6.
### FigS10_Cazyme_genes_ASV_Ratios
The Figure S10 can be accessed [`here`](FigS10_Cazyme_genes_ASV_Ratios). This plot is generated using the code from Figure 6.
