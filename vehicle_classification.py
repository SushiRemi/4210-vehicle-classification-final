#-------------------------------------------------------------------------
# AUTHOR: Julianne Ong, Joseph Scott, Amanda Wong, Anthony Codina, Brandon Trieu, Ameen Saleh
# FILENAME: vehicle_classification.py
# SPECIFICATION: reads training and test data files to create a model to determine whether a car is acceptable, unacceptable, good, or very good
#                based on it's features. Trained using naive bayes.
# FOR: CS 4210- Assignment #2
# TIME SPENT: 11:00AM -> 11:45AM (45 minutes) 
#-----------------------------------------------------------*/


#Importing some Python libraries
from sklearn.naive_bayes import GaussianNB
import csv

#Reading the training data in a csv file
#--> add your Python code here
db = []
X = []
Y = []
header = []

with open('car_training.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
      if i == 0:
         header = row
      elif i > 0: #skipping the header
         db.append (row)

#Transform the original training features to numbers and add them to the 4D array X.
#For instance vhigh = 1, high = 2, med = 3, X = [[3, 1, 1, 2], [1, 3, 2, 2], ...]]

#Transform the original training classes to numbers and add them to the vector Y.
#For instance unacc = 1, acc = 2, so Y = [1, 1, 2, 2, ...]

#--> add your Python code here
for instance in db:
   row = []
   for feature in instance:
      if (feature == "low" or feature == "2" or feature == "small"): 
         row.append(1)
      elif (feature == "med" or feature == "3"):
         row.append(2)
      elif (feature == "high" or feature == "4" or feature == "more" or feature == "big"):
         row.append(3)
      elif (feature == "vhigh" or feature == "5more"):
         row.append(4)
      elif (feature == "unacc"):
         Y.append(0)
      elif (feature == "acc"):
         Y.append(1)
      elif (feature == "good"):
         Y.append(2)
      elif (feature == "vgood"):
         Y.append(3)
   X.append(row)
   if(len(row) != 6):
      print("\f: \f", len(X), len(row))
   

print(Y)

#Fitting the naive bayes to the data
clf = GaussianNB(var_smoothing=1e-9)
clf.fit(X, Y)

#Reading the test data in a csv file
#--> add your Python code here
testdb = []
testX = []
testY = []

with open('car_test.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
      if i > 0: #skipping the header
         testdb.append (row)

trueNumUNACC = 0
trueNumACC = 0
trueNumGOOD = 0
trueNumVGOOD = 0

for instance in testdb:
   row = []
   for feature in instance:
      if (feature == "low" or feature == "2" or feature == "small"): 
         row.append(1)
      elif (feature == "med" or feature == "3"):
         row.append(2)
      elif (feature == "high" or feature == "4" or feature == "more" or feature == "big"):
         row.append(3)
      elif (feature == "vhigh" or feature == "5more"):
         row.append(4)
      elif (feature == "unacc"):
         trueNumUNACC += 1
      elif (feature == "acc"):
         trueNumACC += 1
      elif (feature == "good"):
         trueNumGOOD += 1
      elif (feature == "vgood"):
         trueNumVGOOD += 1
   testX.append(row)



#Printing the header of the solution
#--> add your Python code here
printHeader = ""
for word in header:
   printHeader += word
   printHeader += "\t"
   if(word in ("doors", "persons")):
      printHeader += "\t"
printHeader += "Confidence"
print(printHeader)

#Use your test samples to make probabilistic predictions. For instance: clf.predict_proba([[3, 1, 2, 1]])[0]
#--> add your Python code here
numUNACC = 0
numACC = 0
numGOOD = 0
numVGOOD = 0
numSorted = 0

for instance in range(len(testX)):
   # print(testX[instance])
   probability = clf.predict_proba([testX[instance]])[0]
   # print(probability)
   # if(len(probability) == 4):
   #    print("four found")
   if(probability[0] >= 0.75): #Valid "unacc" class
      numUNACC += 1
      numSorted += 1
      output = ""
      for feature in range(0, (len(testdb[instance]) - 1 )):
         output += testdb[instance][feature]
         output += "\t"
         if(feature == 2 or feature == 3 or feature == 4):
            output += "\t"
      output += "unacc\t\t" 
      output += str(probability[0])
      print(output)
   elif(probability[1] >= 0.75): #Valid "acc" class
      numACC += 1
      numSorted += 1
      output = ""
      for feature in range(0, (len(testdb[instance]) - 1 )):
         output += testdb[instance][feature]
         output += "\t"
         if(feature == 2 or feature == 3 or feature == 4):
            output += "\t"
      output += "acc\t\t" 
      output += str(probability[1])
      print(output)
   elif(probability[2] >= 0.75): #Valid "good" class
      numGOOD += 1
      numSorted += 1
      output = ""
      for feature in range(0, (len(testdb[instance]) - 1 )):
         output += testdb[instance][feature]
         output += "\t"
         if(feature == 2 or feature == 3 or feature == 4):
            output += "\t"
      output += "good\t\t" 
      output += str(probability[2])
      print(output)
   elif(probability[3] >= 0.75): #Valid "vgood" class
      numVGOOD += 1
      numSorted += 1
      output = ""
      for feature in range(0, (len(testdb[instance]) - 1 )):
         output += testdb[instance][feature]
         output += "\t"
         if(feature == 2 or feature == 3 or feature == 4):
            output += "\t"
      output += "vgood\t\t" 
      output += str(probability[3])
      print(output)
      
print("Successfully sorted", numSorted, "out of", len(testX), "instances with 75 percent or greater confidence.")
print("Total Predicted Unacceptable (unacc):", numUNACC, " ||  Total Actual Unacceptable (unacc):", trueNumUNACC)
print("Total Predicted Acceptable (acc):", numACC, " ||  Total Predicted Acceptable (acc):", trueNumACC)
print("Total Predicted Good (good):", numGOOD, " ||  Total Predicted Good (good):", trueNumGOOD)
print("Total Predicted Very Good (vgood):", numVGOOD, " ||  Total Predicted Very Good (vgood):", trueNumVGOOD)
