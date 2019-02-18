import pandas as pd
import re

print('CPSC-51100, Spring 2019')
print("NAME: MICAH WEBB")
print("PROGRAMMING ASSIGNMENT #5" + '\n')


#Read data into data frame
df = pd.read_csv("./cps.csv")

##Define functions for calculated Columns
def get_starthour(row):
    raw = str(row['School_Hours'])
    if raw == 'nan':
        return raw
    else:   
        time_text = re.search('[0-9]:[0-9][0-9]', raw)  #Finds strings like "H:MM"
        if time_text:
            hour = time_text.group(0)[0] #Get the first letter of the first matching expression   
            return hour
        else:
            loose_text = re.search('[0-9] *[aA] *[mM] *-', raw)
            hour = loose_text.group(0)[0] #Get the first letter of the first matching expression   
            return hour


def getLowestGrade(row):
    grades = str(row['Grades_Offered_All']).split(",")[0].strip()
    return grades

def getHighestGrade(row):
    grades = str(row['Grades_Offered_All']).split(",")[::-1][0].strip()    
    return grades

#Apply lambda functions to get calculated columns
df['School_Start_Hour'] = df.apply(lambda row: get_starthour(row), axis=1)
df['Lowest_Grade_Offered'] = df.apply(lambda row: getLowestGrade(row), axis=1)
df['Highest_Grade_Offered'] = df.apply(lambda row: getHighestGrade(row), axis=1)

#Fill in missing College Enrollment values with the mean College Enrollment Rate
df['College_Enrollment_Rate_School'].fillna( (df['College_Enrollment_Rate_School'].mean()), inplace = True, axis = 0)

#Truncate the table to the columns of interest and print results
filtered = df[[
    'School_ID', 
    'Short_Name', 
    'Is_High_School',
    'Zip', 
    'Student_Count_Total',
    'College_Enrollment_Rate_School',
    'Lowest_Grade_Offered',
    'Highest_Grade_Offered',
    'School_Start_Hour'
]]
print(filtered.head(10).to_string(index=False,))

#************* Part 2 *************
#Generate boolean array for high Schools
hs = filtered['Is_High_School'] == True

#Part A - Mean and Standard Deviation of College Enrollment Rate for High Schools
hs_enrollment = filtered.loc[hs]['College_Enrollment_Rate_School']
print('\nCollege Enrollment Rate for High Schools = {:.2f} (sd={:.2f})\n'.format(hs_enrollment.mean(), hs_enrollment.std()))

#Part B - Mean and Standard Deviation of Student_Count_Total for non-high schools
nonHighSchools = filtered.loc[~hs]['Student_Count_Total']
print("Total Student Count for non-High Schools = {:.2f} (sd={:.2f})\n".format(nonHighSchools.mean(), nonHighSchools.std()))


#Part C -Distribution of Starting hours for schools
print("Distribution of Starting Hours")
count_by_start = filtered.groupby('School_Start_Hour').size().sort_values(ascending=False)

for key, value in count_by_start.iteritems():
    if key != 'nan':    
        print(key+'am:', value)

#Part D - Number of Schools outside the loop
#Generate boolean values for loop schools based on list of zip codes
loop_schools = filtered['Zip'].isin((60601,60602,60603,60604,60605,60606,60607,60616))

non_loop_schools = filtered.loc[~loop_schools]
num_nonloop = len(non_loop_schools)
print('\nNumber of schools outside the Loop: {} \n'.format(num_nonloop))