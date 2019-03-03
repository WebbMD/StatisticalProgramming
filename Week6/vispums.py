#######################################################################
# Jeffrey Schult & Micah Webb
# Created on: February 27, 2019
# Micah EDIT: Made plots on right side, edited household count by number of vehicles to use group by,
# CPSC-51100: Statistical Programming
# Spring 1 2019
# Programming Assignment 6 - Visualizing ACS PUMS Data
#######################################################################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

# Read .csv file into panda dataframe
pums_df = pd.read_csv('ss13hil.csv', header=0, usecols=['HHL','HINCP','WGTP', 'VEH','TAXP','VALP', 'MRGP'], skip_blank_lines=True)

# General plot layout adjustments.
plt.rcParams.update({'font.size': 7})
fig1, ax1 = plt.subplots(nrows=2,ncols=2, figsize=(10, 10) )
plt.tight_layout(rect=[0, 0.1, 1.0, 0.8])
plt.subplots_adjust(wspace=0.2,hspace=0.5)

# Provide the figure super title
fig1.suptitle('Sample Output', fontweight='bold', fontsize=12)

# Begin Plot 1 - Household Languages
labels = ['English Only','Spanish','Other Indo-European','Asian and Pacific Island languages','Other']

HHLvalcount = pums_df.HHL.value_counts()

ax1[0,0].pie(HHLvalcount, autopct=None, startangle=242)
ax1[0,0].set_ylabel('HHL')
ax1[0,0].axis('equal')  
ax1[0,0].legend(labels, loc="upper left")
ax1[0,0].set_title('Household Languages')

# Begin Plot 2 - Household income on log scale
# Filter out NaN values and low household income values (some incomes are negative)
income = pums_df['HINCP'][pums_df.HINCP >= 10].dropna()

# Create bins in log scale such that they appear even.
logbins = np.logspace(np.log10(10),np.log10(max(income)), 85)
ax1[0,1].hist(income, bins=logbins, density=True, color = 'green', alpha=0.5) #Plot Histogram

# Create array of values to execute gauss_fit against and plot fitted kde.
gauss_fit = gaussian_kde(income) 
income_range = np.linspace(0, max(income), num= 1000)
ax1[0,1].plot(income_range, gauss_fit(income_range), '--', color = 'black')

# Format Title, labels, axis scale and axis limits
ax1[0,1].set_title('Distribution of Household Income')
ax1[0,1].set_ylabel('Density')
ax1[0,1].set_xlabel('Household Income ($) - Log Scaled')
ax1[0,1].set_xscale('log')
ax1[0,1].set_xlim(7,2*10**7)

# Begin Plot 3
ax1[1,0].set_title('Vehicles Available in Households')
ax1[1,0].set_ylabel('Thousands of Households')
ax1[1,0].set_xlabel('# of Vehicles')

# Use group by operation to sum households with 
veh_group = pums_df.groupby('VEH')
cnt_group = veh_group.sum()/1000
ax1[1,0].bar(cnt_group.index.values, cnt_group.WGTP, color='r')

# Begin Plot 4 
ax1[1,1].set_title('Property Taxes vs. Property Values')
ax1[1,1].set_ylabel('Taxes ($)')
ax1[1,1].set_xlabel('Property Value ($)')
ax1[1,1].set_xlim(0, 1200000)
ax1[1,1].set_ylim(0, 10500)

# Create map of Yearly Taxes Paid to convert from an integer of 1-68 into Taxes paid in $
TAXP_MAP = [0, 1]+[(i-2)*50 for i in range(3,23)]+[100*(j-22) + 1000 for j in range(23, 63)] +[5500, 6000, 7000, 8000, 9000, 10000]

# Create column of Taxes paid yearly ($)
pums_df['TAXP_MAPPED'] = pums_df['TAXP'].apply(lambda x:TAXP_MAP[int(x)-1] if x > 0 else np.nan)

# Filter down data frame into property values less than $1.2 million
tax_prop = pums_df[pums_df['VALP'] < 1200000]

# Reference the scatter plot of Property Value ($) vs Taxes Paid ($) and pass reference to fig1
cax = ax1[1,1].scatter(tax_prop.VALP, tax_prop.TAXP_MAPPED, s = tax_prop.WGTP, marker = 'o', alpha=0.5, c = tax_prop.MRGP, cmap = 'RdBu_r', linewidth = 0.0 )
fig1.colorbar(cax, alpha = 0.5, ticks = [0,1250,2500,3750,5000], label = "First Mortgage Payment Monthly ($)")

# Save plot to png and show plot
plt.savefig("pums.png")
plt.show()