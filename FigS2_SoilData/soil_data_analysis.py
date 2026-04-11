import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import matplotlib.patches as patches

df_soil = pd.read_excel("SoilData_2009_2019-2021.xlsx", dtype={'Experimental_Year': str})

df_soil['Var1'] = df_soil['Var1'].replace({'a2': 'CT', 'a1': 'MP'})
df_soil['Var2'] = df_soil['Var2'].replace({'b3': 'EXT', 'b1': 'INT'})
df_soil['Treatment'] =  df_soil['Var1'] + '-' + df_soil['Var2']

df_soil_grouped = df_soil.groupby(['Treatment', 'Experimental_Year']).agg({'N[%]': 'mean', 'OM[%]': 'mean'})
df_soil_grouped_reset = df_soil_grouped.reset_index()

sns.set_style("whitegrid")
palette = sns.color_palette("Set2")  

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8))

sns.lineplot(data=df_soil_grouped_reset, x='Experimental_Year', y='N[%]', hue='Treatment', ax=ax1, palette=palette[:4], marker='o')
ax1.set_xlabel('')  
ax1.set_ylabel('N (%)',  fontsize=13)
ax1.legend(loc='center left', bbox_to_anchor=(1, -0.1), title='Treatment') 

sns.lineplot(data=df_soil_grouped_reset, x='Experimental_Year', y='OM[%]', hue='Treatment', ax=ax2, palette=palette[:4], marker='o')
ax2.set_xlabel('')  
ax2.set_ylabel('SOM (%)',  fontsize=13)
ax2.get_legend().remove()

#fig.suptitle('Trend Analysis of SOM and N\n(Baseline: 2009, Analysis Period: 2019—2021)', fontsize=14, y=0.95)
fig.suptitle('Trend Analysis of SOM and N', fontsize=14, y=0.95)
fig.text(0.5, 0.91, '(Baseline: 2009; Analysis Period: 2019 — 2021)', ha='center', va='center', fontsize=11)
fig.text(0.5, 0.03, 'Experimental Year', ha='center', va='center', fontsize=13)

plt.subplots_adjust(hspace=0.2, top=0.88, bottom=0.12, right=0.8)


def add_break(ax, start, end, y=0, height=0.001):
    trans = ax.get_xaxis_transform()
    line = patches.FancyBboxPatch(
        (start, y), end - start, height, 
        boxstyle="roundtooth,pad=0.025",
        transform=trans, 
        color='grey', clip_on=False
    )
    ax.add_patch(line)

break_pos1 = 0.475
break_pos2 = 0.525

add_break(ax1, break_pos1, break_pos2)
add_break(ax2, break_pos1, break_pos2)

plt.savefig('FigS2_SoilData.jpg', format='jpeg', dpi=300)
plt.show()

