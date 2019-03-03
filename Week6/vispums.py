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

#Read .csv file into panda dataframe
pums_df = pd.read_csv('ss13hil.csv', header=0, usecols=['HHL','HINCP','WGTP', 'VEH','TAXP','VALP', 'MRGP'], skip_blank_lines=True)



HHLvalcount = pums_df.HHL.value_counts()
WGTPvalcount = pums_df.WGTP.value_counts()
VEHvalcount = pums_df.VEH.value_counts()
# print(VEHvalcount)
# print(WGTPvalcount)


# close open plots
plt.close('all')

# set fontsize in all subplots
plt.rcParams.update({'font.size': 7})

fig1, ax1 = plt.subplots(nrows=2,ncols=2, figsize=(10, 10) )#, subplot_kw=dict(aspect="equal"), figsize=(5,5))

# provide the figure super title
fig1.suptitle('Sample Output', fontweight='bold', fontsize=12)


# Begin Plot 1 - Household Languages

labels = ['English Only','Spanish','Other Indo-European','Asian and Pacific Island languages','Other']

ax1[0,0].pie(HHLvalcount, autopct=None, startangle=242)
ax1[0,0].set_ylabel('HHL')
ax1[0,0].axis('equal')  
ax1[0,0].legend(labels, loc="upper left")
ax1[0,0].set_title('Household Languages')

# End plot 1 


# Begin Plot 2 - Household income on log scale

# Filter out NaN values and low household income values (some incomes are negative)
income = pums_df['HINCP'][pums_df.HINCP >= 10].dropna()

#fit histogram with with gaussian kde, not sure if we are allowed to use scipy, but other options in pandas and seaborn
gauss_fit = gaussian_kde(income) 

#Create non-equal bin sizes such that they look equal on log scale.
#Use max value of Household income as end point. Number of steps will be number of bins
logbins = np.logspace(np.log10(10),np.log10(max(income)), 91)

#Create array of values to execute gauss_fit against.
xs = np.linspace(0, max(income), num= 1000)


ax1[0,1].hist(income, bins=logbins, density=True, color = 'green', alpha=0.5)
ax1[0,1].set_xscale('log') #Set scale to log scale
ax1[0,1].plot(xs, gauss_fit(xs), '--', color = 'black')

ax1[0,1].set_title('Distribution of Household Income')
ax1[0,1].set_ylabel('Density')
ax1[0,1].set_xlabel('Household Income ($) - Log Scaled')
ax1[0,1].set_xlim(7,2*10**7)



#End Plot 2


# Begin Plot 3

vehicles = pums_df['VEH'].dropna()

# loop thru VEH data (NaNs removed) and store the weights in arrays car0, car1, etc. 
'''car0=[]
car1=[]
car2=[]
car3=[]
car4=[]
car5=[]
car6=[]
for i in range(0, len(vehicles)):
    index = vehicles.index[i]
    car = vehicles[index]
    # print(car)
    if car == 0.0:
        # print(pums_df['WGTP'][index])
         car0.append(pums_df['WGTP'][index])
    elif car == 1.0:
         car1.append(pums_df['WGTP'][index])
    elif car == 2.0:
         car2.append(pums_df['WGTP'][index])
    elif car == 3.0:
         car3.append(pums_df['WGTP'][index])  
    elif car == 4.0:
         car4.append(pums_df['WGTP'][index])                     
    elif car == 5.0:
         car5.append(pums_df['WGTP'][index])
    elif car == 6.0:
         car6.append(pums_df['WGTP'][index]) 
                 
#sum the weights and divide by 1000
veh_wgt_cnt = [sum(car0)/1000, sum(car1)/1000, sum(car2)/1000, sum(car3)/1000, sum(car4)/1000, sum(car5)/1000, sum(car6)/1000]

#create x axis array
veh_x_axis = np.sort(VEHvalcount.index)'''

#plot vehicle data
ax1[1,0].set_title('Vehicles Available in Households')
ax1[1,0].set_ylabel('Thousands of Households')
ax1[1,0].set_xlabel('# of Vehicles')

# The loop with the 6 case statements can be replaced by this simple group by operation.
grouped = pums_df.groupby('VEH')
cnt = grouped.sum()/1000
ax1[1,0].bar(cnt.index.values, cnt.WGTP, color='r')
#ax1[1,0].bar(veh_x_axis, veh_wgt_cnt, color='r')


# End Plot 3

# Begin Plot 4 
ax1[1,1].set_title('Property Taxes vs. Property Values')
ax1[1,1].set_ylabel('Taxes ($)')
ax1[1,1].set_xlabel('Property Value ($)')
ax1[1,1].set_xlim(0, 1200000)
ax1[1,1].set_ylim(0, 10500)

#Create map of Yearly Taxes Paid to convert from an integer of 1-68 into Taxes in $
TAXP_MAP = [0, 1]+[(i-2)*50 for i in range(3,23)]+[100*(j-22) + 1000 for j in range(23, 63)] +[5500, 6000, 7000, 8000, 9000, 10000]
#Create column of Taxes paid yearly ($)
pums_df['TAXP_MAPPED'] = pums_df['TAXP'].apply(lambda x:TAXP_MAP[int(x)-1] if x > 0 else np.nan)
#Filter down data frame into property values less than $1.2 million
tax_prop = pums_df[pums_df['VALP'] < 1200000]

#Reference scatter plot of Property Value ($) vs Taxes Paid ($)
cax = ax1[1,1].scatter(tax_prop.VALP, tax_prop.TAXP_MAPPED, s = tax_prop.WGTP, marker = 'o', alpha=0.5, c = tax_prop.MRGP, cmap = 'RdBu_r', linewidth = 0.0 )

#Pass reference of scatter plot to fig1.colorbar() 
fig1.colorbar(cax, alpha = 0.5, ticks = [0,1250,2500,3750,5000], label = "First Mortgage Payment Monthly ($)")
# End Plot 4

# General plot layout adjustments
plt.tight_layout(rect=[0, 0.1, 1.0, 0.8])
plt.subplots_adjust(wspace=0.2,hspace=0.5)

#Save plot to png and show plot
plt.savefig("pums.png")
plt.show()