#######################################################################
# Jeffrey Schult & Micah Webb
# Created on: February 27, 2019
# Micah EDIT:  
# CPSC-51100: Statistical Programming
# Spring 1 2019
# Programming Assignment 6 - Visualizing ACS PUMS Data
#######################################################################
#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

#Read .csv file into panda dataframe
pums_df = pd.read_csv('ss13hil.csv', header=0, usecols=['HHL','HINCP','WGTP', 'VEH','TAXP','VALP', 'MRGI'], skip_blank_lines=False)


#print(pums_df.head(10))

# countHHL = pums_df.groupby('HHL').count()
# print(countHHL)
#print()

HHLvalcount = pums_df.HHL.value_counts()
WGTPvalcount = pums_df.WGTP.value_counts()
VEHvalcount = pums_df.VEH.value_counts()

# print(HHLvalcount)
# print(WGTPvalcount)
# print(VEHvalcount)


fig1, ax1 = plt.subplots(nrows=2,ncols=2 )#, subplot_kw=dict(aspect="equal"), figsize=(5,5))
# plt.subplots_adjust(wspace=0.2,hspace=0.2)
fig1.suptitle('Sample Output', fontweight='bold')


labels = ['English Only','Spanish','Other Indo-European','Asian and Pacific Island languages','Other']
ax1[0,0].pie(HHLvalcount, autopct=None, startangle=242)
ax1[0,0].set_ylabel('HHL')

ax1[0,0].axis('equal')  
ax1[0,0].legend(labels, loc="upper left")
ax1[0,0].set_title('Household Languages')


# Begin Plot 2 - Household income on log scale

# Filter out NaN values and low household income values (some incomes are negative)
income = pums_df['HINCP'][pums_df.HINCP >= 10].dropna()

#fit histogram with with gaussian kde, not sure if we are allowed to use scipy, but other options in pandas and seaborn
gauss_fit = gaussian_kde(income) 

#Create non-equal bin sizes such that they look equal on log scale.
#Use max value of Household income as end point. Number of steps will be number of bins
logbins = np.logspace(np.log10(10),np.log10(max(income)), 100)

#Create array of values to execute gauss_fit against.
xs = np.linspace(10, max(income), num= 1000)

ax1[0,1].hist(income, bins=logbins, density= True, color = 'green')
ax1[0,1].set_xscale('log') #Set scale to log scale
ax1[0,1].plot(xs, gauss_fit(xs), '--', color = 'black')


ax1[0,1].set_title('Distribution of Household Income')
ax1[0,1].set_ylabel('Density')
ax1[0,1].set_xlabel('Household Income ($) - Log Scaled')

#End Plot 2
#%%
vehicles = pums_df['VEH'].dropna()

ax1[1,0].set_title('Vehicles Available in Households')
ax1[1,0].set_ylabel('Thousands of Households')
ax1[1,0].set_xlabel('# of Vehicles')

#%%
ax1[1,1].set_title('Property Taxes vs. Property Values')
ax1[1,1].set_ylabel('Taxes ($)')
ax1[1,1].set_xlabel('Property Value ($)')

tax_prop = pums_df[pums_df.VALP <= 1200000]
ax1[1,1].scatter(tax_prop.VALP, 100*tax_prop.TAXP, s = tax_prop.WGTP, marker = 'o', alpha=0.1, c = tax_prop.MRGI, cmap = 'RdBu')

plt.tight_layout()


plt.show()
