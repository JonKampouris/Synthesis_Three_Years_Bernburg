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

treatments = df_soil_grouped_reset['Treatment'].unique()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8))

sns.lineplot(data=df_soil_grouped_reset, x='Experimental_Year', y='N[%]', hue='Treatment', hue_order=treatments, ax=ax1, palette=palette[:4], marker='o')
ax1.set_xlabel('')  
ax1.set_ylabel('N (%)',  fontsize=13)
ax1.legend(loc='center left', bbox_to_anchor=(1, -0.1), title='Treatment') 

sns.lineplot(data=df_soil_grouped_reset, x='Experimental_Year', y='OM[%]', hue='Treatment', hue_order=treatments, ax=ax2, palette=palette[:4], marker='o')
ax2.set_xlabel('')  
ax2.set_ylabel('SOM (%)',  fontsize=13)
ax2.get_legend().remove()

#fig.suptitle('Trend Analysis of SOM and N\n(Baseline: 2009, Analysis Period: 2019—2021)', fontsize=14, y=0.95)
fig.suptitle('Trend Analysis of SOM and N', fontsize=14, y=0.95)
fig.text(0.5, 0.91, '(Baseline: 2009; Analysis Period: 2019 — 2021)', ha='center', va='center', fontsize=11)
fig.text(0.5, 0.03, 'Experimental Year', ha='center', va='center', fontsize=13)

plt.subplots_adjust(hspace=0.2, top=0.88, bottom=0.12, right=0.8)


def overlay_dashed_segment(ax, y_col):
    tick_labels = [tick.get_text() for tick in ax.get_xticklabels()]
    tick_positions = ax.get_xticks()
    x_positions = {label: pos for label, pos in zip(tick_labels, tick_positions)}

    for treatment in treatments:
        treatment_data = df_soil_grouped_reset[df_soil_grouped_reset['Treatment'] == treatment]
        y_start = treatment_data.loc[treatment_data['Experimental_Year'] == '2009', y_col].iloc[0]
        y_end = treatment_data.loc[treatment_data['Experimental_Year'] == '2019', y_col].iloc[0]
        x0, x1 = x_positions['2009'], x_positions['2019']
        x_mid_start = x0 + 0.35 * (x1 - x0)
        x_mid_end = x0 + 0.65 * (x1 - x0)
        y_mid_start = y_start + 0.35 * (y_end - y_start)
        y_mid_end = y_start + 0.65 * (y_end - y_start)
        ax.plot([x_mid_start, x_mid_end], [y_mid_start, y_mid_end], linestyle='--', color='grey', linewidth=2.5, zorder=15)

overlay_dashed_segment(ax1, 'N[%]')
overlay_dashed_segment(ax2, 'OM[%]')


def get_mid_segment_range(ax, x_start_label='2009', x_end_label='2019', frac_start=0.35, frac_end=0.65):
    tick_labels = [tick.get_text() for tick in ax.get_xticklabels()]
    tick_positions = ax.get_xticks()
    x_positions = {label: pos for label, pos in zip(tick_labels, tick_positions)}
    x0 = x_positions[x_start_label]
    x1 = x_positions[x_end_label]
    x_mid_start = x0 + frac_start * (x1 - x0)
    x_mid_end = x0 + frac_end * (x1 - x0)
    return x_mid_start, x_mid_end


def draw_x_axis_dashed_segment(ax, color='grey'):
    x_mid_start, x_mid_end = get_mid_segment_range(ax)
    ax.plot([x_mid_start, x_mid_end], [0, 0], transform=ax.get_xaxis_transform(),
            color=color, linestyle='--', linewidth=2.5,
            zorder=20, clip_on=False)


def draw_y0_dashed_line(ax, color='grey'):
    ymin, ymax = ax.get_ylim()
    if ymin <= 0 <= ymax:
        x_mid_start, x_mid_end = get_mid_segment_range(ax)
        xlim = ax.get_xlim()
        start_frac = (x_mid_start - xlim[0]) / (xlim[1] - xlim[0])
        end_frac = (x_mid_end - xlim[0]) / (xlim[1] - xlim[0])
        ax.axhline(0, xmin=start_frac, xmax=end_frac, color=color,
                   linestyle='--', linewidth=2.5, zorder=10)


draw_x_axis_dashed_segment(ax1)
draw_x_axis_dashed_segment(ax2)
draw_y0_dashed_line(ax1)
draw_y0_dashed_line(ax2)

plt.savefig('FigS2_SoilData.jpg', format='jpeg', dpi=300)
plt.show()

