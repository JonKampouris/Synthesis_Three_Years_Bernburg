import pandas as pd

#1. Import Raw Data 
df_experimental_setup = pd.read_csv("../../lte_westerfeld.V1_0_EXPERIMENTAL_SETUP.csv")
df_crop = pd.read_csv("../../lte_westerfeld.V1_0_CROP.csv")
df_plant_variety = pd.read_csv("../../lte_westerfeld.V1_0_PLANT_VARIETY.csv")
df_plot = pd.read_csv("../../lte_westerfeld.V1_0_PLOT.csv")

df_crop.loc[df_crop["Crop_ID"] == 5, "Name_EN"] = "Winter wheat 1"
df_crop.loc[df_crop["Crop_ID"] == 4, "Name_EN"] = "Winter wheat 2"

#2. Join Raw Data 
df = pd.merge(
            df_experimental_setup[["Experimental_Year", "Crop_ID", "Plot_ID", "Plant_Variety_ID"]],
            df_crop[["Crop_ID", "Name_EN"]],
            on=["Crop_ID"],
            how="left",
    )

df = df.rename(columns={"Name_EN": "Crop"})

df = pd.merge(
            df,
            df_plant_variety[["Plant_Variety_ID", "Name"]],
            on=["Plant_Variety_ID"],
            how="left",
    )

df = df.rename(columns={"Name": "Plant_Variety"})

df = pd.merge(
            df,
            df_plot[["Plot_ID", "Block"]],
            on=["Plot_ID"],
            how="left",
    )

#3. Filter Raw Data 
df_Year = df[(df["Experimental_Year"] >= 2019) & (df["Experimental_Year"] <= 2021)]
df_reduced = df_Year[~((df_Year['Crop'] == 'Grain maize') & (df_Year['Block'].isin(['C', 'D'])))] 

df_result = df_reduced.drop(
        columns=["Crop_ID", "Plot_ID", "Plant_Variety_ID", "Block", "Experimental_Year"]
).drop_duplicates()

print(df_result)