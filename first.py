import pandas as pd
import numpy as np

data = pd.read_csv('matrix1.csv', sep=',',header=0)
first_name = data["First Name"]
last_name = data["Last Name"]
score = data["Score"]
year = data["Year"]
major = data["Major"]
decision_char = data["Case Interview Decision (Y/N)"]
feedback = data["Feedback"]
decision_int = []

for data in decision_char:
    if data == "Y":
        decision_int.append(1)
    if data == "N":
        decision_int.append(0)

print("Total Applicants: ", len(decision_int))
print("Total Accepted: ", sum(decision_int))
print('Average Acceptance Rate: ', sum(decision_int)/len(decision_int))


#print(data.head())
#print(first_name)p

#https://medium.com/analytics-vidhya/how-to-read-and-write-data-to-google-spreadsheet-using-python-ebf54d51a72c

# https://docs.google.com/spreadsheets/d/1p2kC_knEVd2gVN6a-leyTX7m86tHA0YAuj6H0eal6Z0/edit?usp=sharing
# id: 1p2kC_knEVd2gVN6a-leyTX7m86tHA0YAuj6H0eal6Z0



#https://towardsdatascience.com/how-to-import-google-sheets-data-into-a-pandas-dataframe-using-googles-api-v4-2020-f50e84ea4530