import pandas as pd

print('CPSC-51100, Spring 2019')
print("NAME: MICAH WEBB")
print("PROGRAMMING ASSIGNMENT #4" + '\n')



car_data = pd.read_csv('./cars.csv')

#truncate the columns to just the ones necessary
trunc_data = car_data[['make', 'aspiration']]

#make a data frame of the unique number of makers and set their initial count to zero
unique_makes = pd.DataFrame(data = pd.unique(trunc_data['make']), columns = ['make'])
unique_makes['count'] = 0

#make a data frame of unique aspirations [turbo, std]
unique_aspirations = pd.DataFrame(data = pd.unique(trunc_data['aspiration']), columns = ['aspiration'])


'''Part 1, Conditional probability

Loop through each item in the unique list of manufacturers
Get the total number of rows filtered for that car maker (to be used in the second loop)
Update the count in the unique_makes DataFrame for part 2 of probability calculations.'''

for make in unique_makes.make:

    maker_cnt = trunc_data[trunc_data.make == make].make.count()
    indx = unique_makes[unique_makes.make == make].index[0]
    unique_makes.at[indx, 'count'] = maker_cnt

    for aspiration in unique_aspirations.aspiration:
        asp_maker_cnt = trunc_data[(trunc_data.make == make) & (trunc_data.aspiration == aspiration)].make.count()
        probability = "%.2f%%" % (100*(asp_maker_cnt/maker_cnt))
        print("Prob(aspiration="+aspiration+"|make="+make+") = " + probability)


'''Part 2, probability by manufacturer
print blank line to seperate conditional probability from part 1

Count the total number of rows in full data set
Loop through each specific manufacturer to return row count
Calculate/Print the probability'''

print()
#Calculate total number of data points (rows) in the cars.csv
totrows = trunc_data.count(axis=0)[0]
#loop through each car make and corresponding total for maker and calculate/print out probability
for row in unique_makes.itertuples():
    probability = "%.2f%%" % (100*(row.count/totrows))
    print("Prob(make="+row.make+") = "+ probability )
