#######################################################################
# Micah Webb
# Created on: March 10, 2019
# CPSC-51100: Statistical Programming
# Spring 1 2019
# Programming Assignment 7 - Pivot Tables - ACS PUMS Data
#######################################################################
print('CPSC-51100, Spring 2019')
print("NAME: MICAH WEBB")
print("PROGRAMMING ASSIGNMENT #7" + '\n')
#######################################################################

import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#Load Data
pums_df = pd.read_csv('ss13hil.csv', header=0, usecols=['HHT','HHL','HINCP','WGTP', 'ACCESS'], skip_blank_lines=True)

# Map numeric categories into their appropriate text categories.
access_categories ={1: 'Yes, w/ Subscr.', 2: 'Yes, wo/ Subscr.', 3: 'No'}
HHT_Categories = {
1: 'Married couple household',
2: 'Other family household: Male householder, no wife present',
3: 'Other family household: Female householder, no husband present',
4: 'Nonfamily household: Male householder:Living alone',
5: 'Nonfamily household: Male householder: Not living alone', 
6: 'Nonfamily household: Female householder:Living alone',
7: 'Nonfamily household: Female householder: Not living alone'
}

HHL_Categories = {
1: 'English only', 
2: 'Spanish', 
3: 'Other Indo-European languages' , 
4: 'Asian and Pacific Islan languages', 
5: 'Other' }

pums_df.ACCESS = pums_df.ACCESS.map(access_categories)
pums_df['HHL'] = pums_df['HHL'].map(HHL_Categories)
pums_df['HHT'] = pums_df['HHT'].map(HHT_Categories)

# Table 1
# Statistics of HINCP (Household income past 12 months), grouped by HHT - Household/family type

table = pd.pivot_table(pums_df, values=['HINCP'], index=['HHT'], aggfunc= ('mean', 'std', 'min', 'max', 'count')) 

# Rename index, drop first level of multiindex, cast 'min', 'max' columns as integer types.
table.index.name = 'HHT - Household/family type'
table.columns = table.columns.droplevel()
table['min'] = table['min'].astype(int)
table['max'] = table['max'].astype(int)

print("*** Table 1 - Descriptive Statistics of HINCP, grouped by HHT ***")
print(table[['mean', 'std', 'count', 'min', 'max']].sort_values(by='mean', ascending = False))

# HHL - Household language vs. ACCESS - Access to the Internet (Frequency Table)

# Create table2 dataframe for 'HHL', 'ACCESS', and 'WGTP' columns. Drop Na values
tab2 = pums_df[['HHL', 'ACCESS','WGTP']].dropna()

# Calculate WGTP sum and broadcast back into WGTP column to normalize data
WGTPSUM = tab2['WGTP'].sum()
tab2['WGTP'] = 100*(tab2['WGTP']/WGTPSUM)

# Perform Pivot table sum aggregate operations, include margin column.
table2 = pd.pivot_table(tab2, values=['WGTP'], columns=['ACCESS'], index=['HHL'],margins=True, aggfunc=sum)

# Print table 2, specifying the order of the columns and rows.
# Not sure how to get the top 2 levels of the index to show while being able to sort the columns.
print('\n')
print("*** Table 2 - HHL vs ACCESS - Frequency Table ***")
print(table2.WGTP[[ 'Yes, w/ Subscr.', 'Yes, wo/ Subscr.', 'No', 'All']].sort_values(by='Yes, w/ Subscr.', ascending = False))

# Table 3 - Quantile Analysis of HINCP - Household Income (Past 12 Months) 
pums_df['HINCP_QUANTILES'] = pd.qcut(pums_df['HINCP'], 3, labels=["low", "medium", "high"])

# Perform group by operations on different HINCP_Quantiles
table3 = pd.pivot_table(pums_df, index=['HINCP_QUANTILES'], aggfunc=({'HINCP': ('min', 'max', 'mean'), 'WGTP': sum}))

# Drop top level, rename sum aggregate column to 'household_count', cast 'min', 'max' columns as integer type
table3.columns =  table3.columns.droplevel()
table3.rename(columns={'sum':'household_count'}, inplace=True)
table3.index.name = 'HINCP'
table3['min'] = table3['min'].astype(int)
table3['max'] = table3['max'].astype(int)

# Print table Title and table columns in order
print('\n')
print("*** Table 3 - Quantile Analysis of HINCP - Household Income (Past 12 Months) ***")
print(table3[['min', 'max', 'mean', 'household_count']])