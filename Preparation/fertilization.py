import pandas as pd
from common import prepare_table_experiment

# Load CSV files
df_fertilizer = pd.read_csv("../../lte_westerfeld.V1_0_FERTILIZER.csv")
df_fertilization = pd.read_csv("../../lte_westerfeld.V1_0_FERTILIZATION.csv")

# Add FERTILIZER information
df_fertilization = pd.merge(
    df_fertilization,
    df_fertilizer[["Fertilizer_ID", "Name_EN"]],
    on=["Fertilizer_ID"],
    how="left",
)
df_fertilization = df_fertilization.rename(columns={"Name_EN": "Fertilizer"})

# Drop merged identifier columns
df_fertilization = df_fertilization.drop(columns=["Fertilizer_ID"])


# Add experiment information
df_fertilization = prepare_table_experiment(df_fertilization)

# 1. only 2019, 2020, 2021 are requested 
df_fertilization_reduced_year = df_fertilization[(df_fertilization['Experimental_Year']==2019) | (df_fertilization['Experimental_Year']==2020) | (df_fertilization['Experimental_Year']==2021)]
# 2. filter on Grain Maize 
df_fertilization_reduced_maize = df_fertilization_reduced_year[df_fertilization_reduced_year['Crop']=='Grain maize']
# 3. remove columns not needed
df_fertilization_dropColumns = df_fertilization_reduced_maize.dropna(axis=1, how='all').drop(columns=['Fertilization_ID'
                                                                                                 , 'Date'
                                                                                                 , 'Phosphorus'
                                                                                                 , 'Potassium'
                                                                                                 , 'Crop'
                                                                                                 , 'Plot_ID'
                                                                                                 , 'Tillage'
                                                                                    ]) 
# 4. remove rows not needed
df_fertilization_dropRows = df_fertilization_dropColumns.dropna(subset=['Nitrogen']).copy()

# 5. remove duplicates 
df_fertilization_dropDuplicates = df_fertilization_dropRows.drop_duplicates()

# 6. pivot data 
df_fertilization_pivot = df_fertilization_dropDuplicates.pivot_table(
    index='Experimental_Year',
    columns='Fertilization',
    values='Nitrogen',
    aggfunc='sum'
)

print(df_fertilization_pivot)

