import numpy as np 

print('CPSC-51100, Spring 2019')
print("NAME: MICAH WEBB")
print("PROGRAMMING ASSIGNMENT #3")

#Data Loading function
def load_data(filename):
    raw = np.array([x.rstrip().split(',') for x in open(file = filename, mode = 'r')]) #strip whitespace and split 
    return raw[:, :4].astype(float), raw[:,4].astype(str) #Return tuple Data, Labels

#Load Training and Testing data   
train_dat, train_label = load_data("iris-training-data.csv")
test_dat, test_label = load_data("iris-testing-data.csv")

#Create distance function as lambda and compute distance matrix
dist = lambda point1, point2: np.sqrt(((point1-point2)**2).sum())

#for each point in test data, create list of distances between each point in training data
distance_matrix = np.asarray([[dist(p1, p2) for p2 in train_dat] for p1 in test_dat])

#find the closest neighbor's label by returning index of smallest distance of training data per row.
predicted_label = [train_label[np.argmin(x)] for x in distance_matrix]

#Create list of True/False values by comparing actual label to predicted label
hit_or_miss = predicted_label == test_label

#Accuracy = T / T + F, add 1 for every matching predication and divide by total number of samples
accuracy = 100*sum(1 for boolean in hit_or_miss if boolean)/len(hit_or_miss)


#Print Results
print("#, True, Predicted")
for i in range(0, len(test_label)):
    print(str(i+1), str(test_label[i]), str(predicted_label[i]), sep = ',')

print("Accuracy: " + str(round(accuracy, 2))+"%")