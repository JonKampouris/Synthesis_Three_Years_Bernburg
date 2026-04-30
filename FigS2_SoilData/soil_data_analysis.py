import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import matplotlib.patches as patches
import numpy as np

df_soil = pd.read_excel("SoilData_2009_2019-2021.xlsx", dtype={'Experimental_Year': str})

df_soil['Var1'] = df_soil['Var1'].replace({'a2': 'CT', 'a1': 'MP'})
df_soil['Var2'] = df_soil['Var2'].replace({'b3': 'EXT', 'b1': 'INT'})
df_soil['Treatment'] =  df_soil['Var1'] + '-' + df_soil['Var2']

df_soil_grouped = df_soil.groupby(['Treatment', 'Experimental_Year']).agg({'N[%]': 'mean', 'OM[%]': 'mean'})
df_soil_grouped_reset = df_soil_grouped.reset_index()

sns.set_style("whitegrid")
palette = sns.color_palette("Set2")  

treatments = df_soil_grouped_reset['Treatment'].unique()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8))

# Plot with lines that have a break at the gap markers
def plot_with_gap(ax, data, y_col, treatments, palette):
    """Plot lines with a visual gap between 2009 and 2019"""
    # Get unique years
    years = sorted(data['Experimental_Year'].unique())
    year_positions = {year: i for i, year in enumerate(years)}
    
    for color_idx, treatment in enumerate(treatments):
        treatment_data = data[data['Treatment'] == treatment].sort_values('Experimental_Year')
        
        # Get all data points
        x_all = [year_positions[year] for year in treatment_data['Experimental_Year']]
        y_all = treatment_data[y_col].values
        
        # Plot the full line
        ax.plot(x_all, y_all, 'o-', color=palette[color_idx], label=treatment, linewidth=2, markersize=6)
    
    # Set x-axis labels and ticks
    ax.set_xticks(range(len(years)))
    ax.set_xticklabels(years)
    
    return len(years)

plot_with_gap(ax1, df_soil_grouped_reset, 'N[%]', treatments, palette[:4])
ax1.set_xlabel('')  
ax1.set_ylabel('N (%)',  fontsize=13)
ax1.legend(loc='center left', bbox_to_anchor=(1, -0.1), title='Treatment')

plot_with_gap(ax2, df_soil_grouped_reset, 'OM[%]', treatments, palette[:4])
ax2.set_xlabel('')  
ax2.set_ylabel('SOM (%)',  fontsize=13)

fig.suptitle('Trend analysis of SOM and N', fontsize=14, y=0.95)
fig.text(0.5, 0.91, '(Baseline: 2009; Analysis period: 2019 — 2021)', ha='center', va='center', fontsize=11)
fig.text(0.5, 0.03, 'Experimental year', ha='center', va='center', fontsize=13)

plt.subplots_adjust(hspace=0.2, top=0.88, bottom=0.12, right=0.8)

# Add gap markers (diagonal slashes) and break the lines
def add_gap_with_broken_lines(ax):
    """Add diagonal slash marks and break lines at the gap position"""
    ymin, ymax = ax.get_ylim()
    y_range = ymax - ymin
    x_gap = 0.5  # Position between 2009 (0) and 2019 (1)
    
    # Draw two diagonal lines to indicate a gap
    ax.plot([x_gap - 0.08, x_gap - 0.02], [ymin - 0.02*y_range, ymin + 0.02*y_range], 
            'k-', linewidth=1.5, clip_on=False, zorder=101)
    ax.plot([x_gap + 0.02, x_gap + 0.08], [ymin - 0.02*y_range, ymin + 0.02*y_range], 
            'k-', linewidth=1.5, clip_on=False, zorder=101)
    
    # Create a white rectangle to "break" the lines - spanning full height
    gap_width = 0.25
    from matplotlib.patches import Rectangle
    rect = Rectangle((x_gap - gap_width/2, ymin), gap_width, y_range, 
                      facecolor='white', edgecolor='white', linewidth=0, zorder=100)
    ax.add_patch(rect)

# Add gap markers and broken lines to both subplots
add_gap_with_broken_lines(ax1)
add_gap_with_broken_lines(ax2)

plt.savefig('FigS2_SoilData.jpg', format='jpeg', dpi=300)
plt.show()

