import pandas as pd
from common import prepare_table_experiment
import numpy as np

# Load CSV files
df_soil_lab = pd.read_csv("../../lte_westerfeld.V1_0_SOIL_LAB.csv")
df_soil_sampling = pd.read_csv("../../lte_westerfeld.V1_0_SOIL_SAMPLING.csv")
df_beneficial = pd.read_csv("../../lte_westerfeld.V1_0_BENEFICIAL.csv")
df_plot =pd.read_csv("../../lte_westerfeld.V1_0_PLOT.csv")


# Add SOIL_SAMPLING information
df_soil_lab = pd.merge(
    df_soil_lab, df_soil_sampling, on=["Soil_Sampling_ID"], how="left"
)

# Add BENEFICIAL information
df_soil_lab = pd.merge(
    df_soil_lab,
    df_beneficial[["Beneficial_ID", "Name_EN"]],
    on=["Beneficial_ID"],
    how="left",
)
df_soil_lab = df_soil_lab.rename(columns={"Name_EN": "Beneficial"})

# Add PLOT information
df_soil_lab = pd.merge(
    df_soil_lab,
    df_plot[["Plot_ID", "Block", "Replication"]],
    on=["Plot_ID"],
    how="left",
)


# Drop merged identifier columns
df_soil_lab = df_soil_lab.drop(columns=["Beneficial_ID", "Soil_Sampling_ID"])

# Add experiment information
df_soil_lab = prepare_table_experiment(df_soil_lab)

#************************************************************************
#  Preparation for Collaboration with JKI
#************************************************************************

# 1. only 2019, 2020, 2021 are requested 
df_soil_lab_reduced_year = df_soil_lab[(df_soil_lab['Experimental_Year']==2019) | (df_soil_lab['Experimental_Year']==2020) | (df_soil_lab['Experimental_Year']==2021)]
# 2. only Beneficial = "Control" data should be used 
df_soil_lab_reduced_beneficial = df_soil_lab_reduced_year[df_soil_lab_reduced_year['Beneficial']=='Control']
# 3. filter on Grain Maize 
df_soil_lab_maize = df_soil_lab_reduced_beneficial[df_soil_lab_reduced_beneficial['Crop']=='Grain maize']
# 4. remove columns not needed
df_soil_lab_dropColumns = df_soil_lab_maize.dropna(axis=1, how='all').drop(columns=['WHC'
                                                                                                 , 'Depth_min'
                                                                                                 , 'Depth_max'
                                                                                                 , 'Beneficial'
                                                                                                 , 'Soil_Lab_ID'
                                                                                                 , 'Plot_ID'
                                                                                                 , 'Crop'
                                                                                    ]) 
# 5. remove rows not needed
df_soil_lab_dropRows = df_soil_lab_dropColumns.dropna(thresh=11).copy()
# 6. Total Carbon is missing in the raw data 2021. 
df_soil_lab_dropRows.loc[df_soil_lab_dropRows['Experimental_Year'] == 2021, 'Total_Carbon'] = np.nan
df_soil_lab_dropRows.loc[df_soil_lab_dropRows['Experimental_Year'] == 2021, 'CN_Ratio'] = np.nan
# 7. concatenate Block and Replication columns
df_soil_lab_dropRows['Block'] = df_soil_lab_dropRows['Block'] + df_soil_lab_dropRows['Replication'].astype(str)
df_soil_lab_dropRep = df_soil_lab_dropRows.drop(columns=['Replication'])
# 8. reorder columns 
last_8_columns = df_soil_lab_dropRep.columns[-5:]
first_15_columns = df_soil_lab_dropRep.columns[:-5]
new_order = last_8_columns.tolist() + first_15_columns.tolist()
df_soil_lab_reordered = df_soil_lab_dropRep[new_order]
# 9. drop incomplete columns with missing data over the years 
df_soil_lab_dropColumns_2 = df_soil_lab_reordered.drop(columns=[  'Borium' # only in 2021
                                                                , 'Sulphate' # only in 2021
                                                                , 'Calcium' # not in 2021
                                                        ])

# 10. Add missing data (Total Carbon and C/N Ratio in 2021)
condition = df_soil_lab_dropColumns_2['Experimental_Year'] == 2021
df_soil_lab_dropColumns_2.loc[condition, 'Total_Carbon'] = df_soil_lab_dropColumns_2.loc[condition, 'Organic_Matter'] / 1.724
df_soil_lab_dropColumns_2.loc[condition, 'CN_Ratio'] = df_soil_lab_dropColumns_2.loc[condition, 'Total_Carbon'] / df_soil_lab_dropColumns_2.loc[condition, 'Total_Nitrogen'] 

# 11. rename columns as in R script requested 
df_soil_lab_final = df_soil_lab_dropColumns_2.rename(columns={
                                                   "CN_Ratio": "C/N"	
                                                 , "Total_Carbon": "C[%]"
                                                 , "Total_Nitrogen": "N[%]"
                                                 , "Iron": "Fe[mg/100g]"	
                                                 , "Potassium_Oxide": "K2O[mg/100g]"
                                                 , "Copper": "Cu[mg/kg]"	
                                                 , "Magnesium": "Mg[mg/100g]"
                                                 , "Manganese": "Mn[mg/kg]"	
                                                 , "Sodium": "Na[mg/kg]"	
                                                 , "Ammonium": "NH4-N[mg/100g]"	
                                                 , "Nitrate": "NO3-N[mg/100g]"	
                                                 , "Organic_Matter": "OM[%]"	
                                                 , "Diphosphorus_Pentoxide": "P2O5[mg/100g]"
                                                 , "Dry_Matter": "DM[%]"	
                                                 , "Zinc": "Zn[mg/kg]"                                                
                                                 })

# Export data to excel
df_soil_lab_final.to_excel("soil_lab.xlsx", index=False)
# Export data to csv
df_soil_lab_final.to_csv("soil_lab.csv", index=False)
