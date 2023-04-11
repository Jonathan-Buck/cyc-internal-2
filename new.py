import os
import pandas as pd
import numpy as np
import re



def storeCSV(matrix_name, application_name, semester):
    # Dataframe we are putting everything into
    df = pd.DataFrame(columns=['Applicant_Name', 'Semester', 'Interviewers', 'Each_Matrix_Num'])
    #, 'Round_Decision', 'Q1_Feedback', 'Q2_Feedback', 'Q3_Feedback', 'Notes', 'Major', 'Minor', 'Ethnicity', 'Gender', 'Recommend', 'GPA', 'Expected_Grad'


    matrix = pd.read_csv(matrix_name, sep=',',header=0)

    print(len(matrix)) # rows
    print(len(matrix.columns)) # columns

    # print(data.info())

    # print(data.head)
    # print(data.iloc[:,3])
    # print(data.iloc[:,4])

    # main_matrix.csv data collection
    for cols in range(3,len(matrix.columns),2):
        if (pd.isnull(matrix.iloc[0,cols]) and pd.isnull(matrix.iloc[1,cols + 1])):
            break
        # print(matrix.iloc[0,cols])
        # print(matrix.iloc[1,cols + 1])
        # ------------------------------------------------------------------------------------
        # This loop goes through the applicant name and removes any nickname within parantheses
        name_array = matrix.iloc[0,cols].split()
        applicant_name = ""
        for name in name_array:
            if "(" not in name:
                applicant_name += name + " "
        applicant_name = applicant_name[:len(applicant_name) - 1]
        print(applicant_name)
        # -------------------------------------------------------------------------------------

        interviwers = [matrix.columns[cols], matrix.columns[cols + 1]]
        matrix_percent = [matrix.iloc[len(matrix) - 1, cols ], matrix.iloc[len(matrix) - 1, cols + 1]]
        # index      applicant name     interviewers
        df.loc[len(df.index)] = [applicant_name, semester, interviwers, matrix_percent]
    # ----------------------------------------------------------------------------

    decisions = pd.read_csv(application_name, sep=',',header=0)
    # print(decisions.head())
    # print(decisions.iloc[33,0] + decisions.iloc[33, 1])
    # print(decisions.iloc[1, 1])
    # print(len(decisions))

    print("part 2")

    # add the other desired data columns to the dataframe and initialize to null
    df["GPA"] = np.nan
    df["Round_Decision"] = np.nan
    df["Round_Decision_Quantified"] = np.nan
    df["Notes"] = np.nan
    df["Major"] = np.nan
    df["Minor"] = np.nan
    df["Ethnicity"] = np.nan
    df["Ethnicity_Quantified"] = np.nan
    df["Gender"] = np.nan
    df["Gender_Quantified"] = np.nan
    #df["Recommend"] = [[] for _ in range(len(df))]
    df["Recommend1"] = np.nan
    df["Recommend2"] = np.nan
    df["Recommend1_Quantified"] = np.nan
    df["Recommend2_Quantified"] = np.nan
    df["Grad_Year"] = np.nan

    # for each row in the decisions matrix
    column_names = decisions.columns.values.tolist()
    first_name = column_names.index('First Name')
    last_name = column_names.index('Last Name')
    print(first_name)
    print(last_name)
    for entries in range(0, len(decisions)):
        # if the row is not null
        if not pd.isna(decisions.iloc[entries,0]):
            #print(decisions.iloc[entries,0] + decisions.iloc[entries, 1])
            # set the applicant name for the row to a reference variable used to query the dataframe
            entry_name = decisions.iloc[entries, first_name] + " " + decisions.iloc[entries, last_name]
            # query the dataframe to find the index corresponding to the applicant
            index = df.index[df['Applicant_Name'] == entry_name]
            # for each desired datapoint add the datapoint into the dataframe at the correct index
            df.loc[index, 'GPA'] = decisions.iloc[entries,9]
            df.loc[index, 'Round_Decision'] = decisions.iloc[entries,23]
            if(decisions.iloc[entries,23] == "Reject" or decisions.iloc[entries,23] == "Reject and Reapply"):
                df.loc[index, 'Round_Decision_Quantified'] = 0
            elif(decisions.iloc[entries,23] == "Accept"):
                df.loc[index, 'Round_Decision_Quantified'] = 1
            df.loc[index, 'Notes'] = decisions.iloc[entries,24]
            df.loc[index, 'Major'] = decisions.iloc[entries,5]
            df.loc[index, 'Minor'] = decisions.iloc[entries,6]
            df.loc[index, 'Ethnicity'] = decisions.iloc[entries,12]
            if(decisions.iloc[entries,12] == "I do not wish to disclose."):
                df.loc[index, 'Ethnicity_Quantified'] = 0
            elif(decisions.iloc[entries,12] == "Asian: A person having origins in any of the original peoples of the Far East, Southeast Asia or the Indian Subcontinent, including, for example, Cambodia, China, India, Japan, Korea, Malaysia, Pakistan, the Philippine Islands, Thailand and Vietnam."):
                df.loc[index, 'Ethnicity_Quantified'] = 1
            elif(decisions.iloc[entries,12] == "White: A person having origins in any of the original peoples of Europe, the Middle East or North Africa."):
                df.loc[index, 'Ethnicity_Quantified'] = 2
            elif(decisions.iloc[entries,12] == "Black or African American: A person having origins in any of the black racial groups of Africa."):
                df.loc[index, 'Ethnicity_Quantified'] = 3
            if(decisions.iloc[entries,12] == "Hispanic or Latino: A person of Cuban, Mexican, Puerto Rican, South or Central American, or other Spanish culture or origin regardless of race."):
                df.loc[index, 'Ethnicity_Quantified'] = 4     
            df.loc[index, 'Gender'] = decisions.iloc[entries,13]
            if(decisions.iloc[entries,13] == "I do not wish to disclose."):
                df.loc[index, 'Gender_Quantified'] = 0
            elif(decisions.iloc[entries,13] == "Male"):
                df.loc[index, 'Gender_Quantified'] = 1
            elif(decisions.iloc[entries,13] == "Female"):
                df.loc[index, 'Gender_Quantified'] = 2
            df.loc[index, 'Recommend1'] = decisions.iloc[entries,14]
            if(decisions.iloc[entries,14] == "Do Not Recommend"):
                df.loc[index, 'Recommend1_Quantified'] = 0
            elif(decisions.iloc[entries,14] == "Recommend with Hesitation"):
                df.loc[index, 'Recommend1_Quantified'] = 1
            elif(decisions.iloc[entries,14] == "Recommend"):
                df.loc[index, 'Recommend1_Quantified'] = 2
            elif(decisions.iloc[entries,14] == "Strongly Recommend"):
                df.loc[index, 'Recommend1_Quantified'] = 3
            df.loc[index, 'Recommend2'] = decisions.iloc[entries,15]
            if(decisions.iloc[entries,15] == "Do Not Recommend"):
                df.loc[index, 'Recommend2_Quantified'] = 0
            elif(decisions.iloc[entries,15] == "Recommend with Hesitation"):
                df.loc[index, 'Recommend2_Quantified'] = 1
            elif(decisions.iloc[entries,15] == "Recommend"):
                df.loc[index, 'Recommend2_Quantified'] = 2
            elif(decisions.iloc[entries,15] == "Strongly Recommend"):
                df.loc[index, 'Recommend2_Quantified'] = 3
            df.loc[index, 'Grad_Year'] = decisions.iloc[entries,8]
        



    print(df)

    print(df[['Round_Decision']].to_string(index=False))

    df.to_csv('complete.csv', index=False)




matrix_name = ""
application_name = ""
year = ""




# Define the pattern to search for
spring = r'Spring\s+\d{4}'
fall = r'Fall\s+\d{4}'


# Set the directory path
dir_path = 'interview_data'

# Sort Directory
file_list = sorted(os.listdir(dir_path))

# Loop through all the files in the directory

# for files in range(0, len(file_list),2):
#     application = file_list[files]
#     matrix = file_list[files + 1]

#     # Read the CSV file into a pandas DataFrame
#     matrix_name = os.path.join(dir_path, matrix)
#     application_name = os.path.join(dir_path, application)

#     #---- Finding for the Spring and year using regex
#     # Search for the pattern in the string
#     spring_match = re.search(spring, matrix_name)

#     # If a match is found, extract the matched substring
#     if spring_match:
#         year = spring_match.group(0)

#     #---- Finding for the Fall and year using regex
#     # Search for the pattern in the string
#     fall_match = re.search(fall, matrix_name)

#     # If a match is found, extract the matched substring
#     if fall_match:
#         year = fall_match.group(0)
#     print(year)
#     storeCSV(matrix_name, application_name, year)




def fall2020(matrix_name, application_name, semester):
    # Dataframe we are putting everything into
    df = pd.DataFrame(columns=['Applicant_Name', 'Semester', 'Interviewers', 'Each_Matrix_Num'])
    #, 'Round_Decision', 'Q1_Feedback', 'Q2_Feedback', 'Q3_Feedback', 'Notes', 'Major', 'Minor', 'Ethnicity', 'Gender', 'Recommend', 'GPA', 'Expected_Grad'


    matrix = pd.read_csv(matrix_name, sep=',',header=0)

    print(len(matrix)) # rows
    print(len(matrix.columns)) # columns

    # print(data.info())

    # print(data.head)
    # print(data.iloc[:,3])
    # print(data.iloc[:,4])

    # main_matrix.csv data collection
    for cols in range(3,len(matrix.columns),2):
        if (pd.isnull(matrix.iloc[0,cols]) and pd.isnull(matrix.iloc[1,cols + 1])):
            break
        # print(matrix.iloc[0,cols])
        # print(matrix.iloc[1,cols + 1])
        # ------------------------------------------------------------------------------------
        # This loop goes through the applicant name and removes any nickname within parantheses
        name_array = matrix.iloc[0,cols].split()
        applicant_name = ""
        for name in name_array:
            if "(" not in name:
                applicant_name += name + " "
        applicant_name = applicant_name[:len(applicant_name) - 1]
        print(applicant_name)
        # -------------------------------------------------------------------------------------

        interviwers = [matrix.columns[cols], matrix.columns[cols + 1]]
        matrix_percent = [matrix.iloc[len(matrix) - 1, cols ], matrix.iloc[len(matrix) - 1, cols + 1]]
        # index      applicant name     interviewers
        df.loc[len(df.index)] = [applicant_name, semester, interviwers, matrix_percent]
    # ----------------------------------------------------------------------------
    df["GPA"] = np.nan
    df["Round_Decision"] = np.nan
    df["Round_Decision_Quantified"] = np.nan
    df["Notes"] = np.nan
    df["Major"] = np.nan
    df["Minor"] = np.nan
    df["Ethnicity"] = np.nan
    df["Ethnicity_Quantified"] = np.nan
    df["Gender"] = np.nan
    df["Gender_Quantified"] = np.nan
    #df["Recommend"] = [[] for _ in range(len(df))]
    df["Recommend1"] = np.nan
    df["Recommend2"] = np.nan
    df["Recommend1_Quantified"] = np.nan
    df["Recommend2_Quantified"] = np.nan
    df["Grad_Year"] = np.nan


    decisions = pd.read_csv(application_name, sep=',',header=0)

    column_names = decisions.columns.values.tolist()
    first_name = column_names.index('First Name')
    last_name = column_names.index('Last Name')
    major = column_names.index('Major(s)')
    gpa = column_names.index('Cumulative GPA')
    reccomend1 = column_names.index('Recommendation 1')
    reccomend2 = column_names.index('Recommendation 2')
    notes = column_names.index('Notes')
    decision = column_names.index('Decision')
    graduation = column_names.index('Expected Graduation')

    
    for entries in range(0, len(decisions)):
        # if the row is not null
        if not pd.isna(decisions.iloc[entries,0]):
            #print(decisions.iloc[entries,0] + decisions.iloc[entries, 1])
            # set the applicant name for the row to a reference variable used to query the dataframe
            entry_name = decisions.iloc[entries, first_name].strip() + " " + decisions.iloc[entries, last_name].strip()
            print(entry_name)
            # query the dataframe to find the index corresponding to the applicant
            index = df.index[df['Applicant_Name'] == entry_name]
            # for each desired datapoint add the datapoint into the dataframe at the correct index
            df.loc[index, 'GPA'] = decisions.iloc[entries,gpa]
            df.loc[index, 'Round_Decision'] = decisions.iloc[entries,decision]
            if(decisions.iloc[entries,decision] == "Reject" or decisions.iloc[entries,decision] == "Reject and Reapply"):
                df.loc[index, 'Round_Decision_Quantified'] = 0
            elif(decisions.iloc[entries,decision] == "Accept"):
                df.loc[index, 'Round_Decision_Quantified'] = 1
            df.loc[index, 'Notes'] = decisions.iloc[entries,notes]
            df.loc[index, 'Major'] = decisions.iloc[entries,major]
            # df.loc[index, 'Minor'] = decisions.iloc[entries,6]
            # df.loc[index, 'Ethnicity'] = decisions.iloc[entries,12]
            # if(decisions.iloc[entries,12] == "I do not wish to disclose."):
            #     df.loc[index, 'Ethnicity_Quantified'] = 0
            # elif(decisions.iloc[entries,12] == "Asian: A person having origins in any of the original peoples of the Far East, Southeast Asia or the Indian Subcontinent, including, for example, Cambodia, China, India, Japan, Korea, Malaysia, Pakistan, the Philippine Islands, Thailand and Vietnam."):
            #     df.loc[index, 'Ethnicity_Quantified'] = 1
            # elif(decisions.iloc[entries,12] == "White: A person having origins in any of the original peoples of Europe, the Middle East or North Africa."):
            #     df.loc[index, 'Ethnicity_Quantified'] = 2
            # elif(decisions.iloc[entries,12] == "Black or African American: A person having origins in any of the black racial groups of Africa."):
            #     df.loc[index, 'Ethnicity_Quantified'] = 3
            # if(decisions.iloc[entries,12] == "Hispanic or Latino: A person of Cuban, Mexican, Puerto Rican, South or Central American, or other Spanish culture or origin regardless of race."):
            #     df.loc[index, 'Ethnicity_Quantified'] = 4     
            # df.loc[index, 'Gender'] = decisions.iloc[entries,13]
            # if(decisions.iloc[entries,13] == "I do not wish to disclose."):
            #     df.loc[index, 'Gender_Quantified'] = 0
            # elif(decisions.iloc[entries,13] == "Male"):
            #     df.loc[index, 'Gender_Quantified'] = 1
            # elif(decisions.iloc[entries,13] == "Female"):
            #     df.loc[index, 'Gender_Quantified'] = 2
            df.loc[index, 'Recommend1'] = decisions.iloc[entries,reccomend1]
            if(decisions.iloc[entries,reccomend1] == "Do Not Recommend"):
                df.loc[index, 'Recommend1_Quantified'] = 0
            elif(decisions.iloc[entries,reccomend1] == "Recommend with Hesitation"):
                df.loc[index, 'Recommend1_Quantified'] = 1
            elif(decisions.iloc[entries,reccomend1] == "Recommend"):
                df.loc[index, 'Recommend1_Quantified'] = 2
            elif(decisions.iloc[entries,reccomend1] == "Strongly Recommend"):
                df.loc[index, 'Recommend1_Quantified'] = 3
            df.loc[index, 'Recommend2'] = decisions.iloc[entries,reccomend2]
            if(decisions.iloc[entries,reccomend2] == "Do Not Recommend"):
                df.loc[index, 'Recommend2_Quantified'] = 0
            elif(decisions.iloc[entries,reccomend2] == "Recommend with Hesitation"):
                df.loc[index, 'Recommend2_Quantified'] = 1
            elif(decisions.iloc[entries,reccomend2] == "Recommend"):
                df.loc[index, 'Recommend2_Quantified'] = 2
            elif(decisions.iloc[entries,reccomend2] == "Strongly Recommend"):
                df.loc[index, 'Recommend2_Quantified'] = 3
            df.loc[index, 'Grad_Year'] = decisions.iloc[entries,graduation]

    df.to_csv('complete.csv', index=False)


fall2020("interview_data/Copy of Behavioral Interview Matrix Fall 2020 - Matrix.csv","interview_data/Copy of Behavioral Interview Matrix Fall 2020 - Decisons.csv", "Fall 2020")


def fall2021(matrix_name, application_name, semester):
    # Dataframe we are putting everything into
    df = pd.DataFrame(columns=['Applicant_Name', 'Semester', 'Interviewers', 'Each_Matrix_Num'])
    #, 'Round_Decision', 'Q1_Feedback', 'Q2_Feedback', 'Q3_Feedback', 'Notes', 'Major', 'Minor', 'Ethnicity', 'Gender', 'Recommend', 'GPA', 'Expected_Grad'


    matrix = pd.read_csv(matrix_name, sep=',',header=0)

    print(len(matrix)) # rows
    print(len(matrix.columns)) # columns

    # print(data.info())

    # print(data.head)
    # print(data.iloc[:,3])
    # print(data.iloc[:,4])

    # main_matrix.csv data collection
    for cols in range(3,len(matrix.columns),2):
        if (pd.isnull(matrix.iloc[0,cols]) and pd.isnull(matrix.iloc[1,cols + 1])):
            break
        # print(matrix.iloc[0,cols])
        # print(matrix.iloc[1,cols + 1])
        # ------------------------------------------------------------------------------------
        # This loop goes through the applicant name and removes any nickname within parantheses
        name_array = matrix.iloc[0,cols].split()
        applicant_name = ""
        for name in name_array:
            if "(" not in name:
                applicant_name += name + " "
        applicant_name = applicant_name[:len(applicant_name) - 1]
        print(applicant_name)
        # -------------------------------------------------------------------------------------

        interviwers = [matrix.columns[cols], matrix.columns[cols + 1]]
        matrix_percent = [matrix.iloc[len(matrix) - 1, cols ], matrix.iloc[len(matrix) - 1, cols + 1]]
        # index      applicant name     interviewers
        df.loc[len(df.index)] = [applicant_name, semester, interviwers, matrix_percent]
    # ----------------------------------------------------------------------------
    df["GPA"] = np.nan
    df["Round_Decision"] = np.nan
    df["Round_Decision_Quantified"] = np.nan
    df["Notes"] = np.nan
    df["Major"] = np.nan
    df["Minor"] = np.nan
    df["Ethnicity"] = np.nan
    df["Ethnicity_Quantified"] = np.nan
    df["Gender"] = np.nan
    df["Gender_Quantified"] = np.nan
    #df["Recommend"] = [[] for _ in range(len(df))]
    df["Recommend1"] = np.nan
    df["Recommend2"] = np.nan
    df["Recommend1_Quantified"] = np.nan
    df["Recommend2_Quantified"] = np.nan
    df["Grad_Year"] = np.nan


    decisions = pd.read_csv(application_name, sep=',',header=0)

    column_names = decisions.columns.values.tolist()
    print(column_names)
    first_name = column_names.index('First Name ')
    last_name = column_names.index('Last Name')
    major = column_names.index('Major(s)')
    minor = column_names.index('Minor(s)')
    gpa = column_names.index('Cumulative GPA')
    gender = column_names.index('What is your gender?')
    ethnicity = column_names.index('What is your race/ethnicity?')
    # reccomend1 = column_names.index('Recommendation 1')
    # reccomend2 = column_names.index('Recommendation 2')
    # notes = column_names.index('Notes')
    # decision = column_names.index('Decision')
    graduation = column_names.index('Expected Graduation')

    for entries in range(0, len(decisions)):
        # if the row is not null
        if not pd.isna(decisions.iloc[entries,0]):
            #print(decisions.iloc[entries,0] + decisions.iloc[entries, 1])
            # set the applicant name for the row to a reference variable used to query the dataframe
            entry_name = decisions.iloc[entries, first_name].strip() + " " + decisions.iloc[entries, last_name].strip()
            print(entry_name)
            # query the dataframe to find the index corresponding to the applicant
            index = df.index[df['Applicant_Name'] == entry_name]
            # for each desired datapoint add the datapoint into the dataframe at the correct index
            df.loc[index, 'GPA'] = decisions.iloc[entries,gpa]
            # df.loc[index, 'Round_Decision'] = decisions.iloc[entries,decision]
            # if(decisions.iloc[entries,decision] == "Reject" or decisions.iloc[entries,decision] == "Reject and Reapply"):
            #     df.loc[index, 'Round_Decision_Quantified'] = 0
            # elif(decisions.iloc[entries,decision] == "Accept"):
            #     df.loc[index, 'Round_Decision_Quantified'] = 1
            # df.loc[index, 'Notes'] = decisions.iloc[entries,notes]
            df.loc[index, 'Major'] = decisions.iloc[entries,major]
            df.loc[index, 'Minor'] = decisions.iloc[entries,minor]
            df.loc[index, 'Ethnicity'] = decisions.iloc[entries,ethnicity]
            if(decisions.iloc[entries,ethnicity] == "I do not wish to disclose."):
                df.loc[index, 'Ethnicity_Quantified'] = 0
            elif(decisions.iloc[entries,ethnicity] == "Asian: A person having origins in any of the original peoples of the Far East, Southeast Asia or the Indian Subcontinent, including, for example, Cambodia, China, India, Japan, Korea, Malaysia, Pakistan, the Philippine Islands, Thailand and Vietnam."):
                df.loc[index, 'Ethnicity_Quantified'] = 1
            elif(decisions.iloc[entries,ethnicity] == "White: A person having origins in any of the original peoples of Europe, the Middle East or North Africa."):
                df.loc[index, 'Ethnicity_Quantified'] = 2
            elif(decisions.iloc[entries,ethnicity] == "Black or African American: A person having origins in any of the black racial groups of Africa."):
                df.loc[index, 'Ethnicity_Quantified'] = 3
            if(decisions.iloc[entries,ethnicity] == "Hispanic or Latino: A person of Cuban, Mexican, Puerto Rican, South or Central American, or other Spanish culture or origin regardless of race."):
                df.loc[index, 'Ethnicity_Quantified'] = 4     
            df.loc[index, 'Gender'] = decisions.iloc[entries,gender]
            if(decisions.iloc[entries,gender] == "I do not wish to disclose."):
                df.loc[index, 'Gender_Quantified'] = 0
            elif(decisions.iloc[entries,gender] == "Male"):
                df.loc[index, 'Gender_Quantified'] = 1
            elif(decisions.iloc[entries,gender] == "Female"):
                df.loc[index, 'Gender_Quantified'] = 2
            # df.loc[index, 'Recommend1'] = decisions.iloc[entries,reccomend1]
            # if(decisions.iloc[entries,reccomend1] == "Do Not Recommend"):
            #     df.loc[index, 'Recommend1_Quantified'] = 0
            # elif(decisions.iloc[entries,reccomend1] == "Recommend with Hesitation"):
            #     df.loc[index, 'Recommend1_Quantified'] = 1
            # elif(decisions.iloc[entries,reccomend1] == "Recommend"):
            #     df.loc[index, 'Recommend1_Quantified'] = 2
            # elif(decisions.iloc[entries,reccomend1] == "Strongly Recommend"):
            #     df.loc[index, 'Recommend1_Quantified'] = 3
            # df.loc[index, 'Recommend2'] = decisions.iloc[entries,reccomend2]
            # if(decisions.iloc[entries,reccomend2] == "Do Not Recommend"):
            #     df.loc[index, 'Recommend2_Quantified'] = 0
            # elif(decisions.iloc[entries,reccomend2] == "Recommend with Hesitation"):
            #     df.loc[index, 'Recommend2_Quantified'] = 1
            # elif(decisions.iloc[entries,reccomend2] == "Recommend"):
            #     df.loc[index, 'Recommend2_Quantified'] = 2
            # elif(decisions.iloc[entries,reccomend2] == "Strongly Recommend"):
            #     df.loc[index, 'Recommend2_Quantified'] = 3
            df.loc[index, 'Grad_Year'] = decisions.iloc[entries,graduation]

    df.to_csv('complete1.csv', index=False)


fall2021("interview_data/Copy of Behavioral Interview Matrix Fall 2021 - Matrix.csv","interview_data/Copy of Behavioral Interview Matrix Fall 2021 - Applications.csv", "Fall 2021")


def fall2022(matrix_name, application_name, semester):
    # Dataframe we are putting everything into
    df = pd.DataFrame(columns=['Applicant_Name', 'Semester', 'Interviewers', 'Each_Matrix_Num'])
    #, 'Round_Decision', 'Q1_Feedback', 'Q2_Feedback', 'Q3_Feedback', 'Notes', 'Major', 'Minor', 'Ethnicity', 'Gender', 'Recommend', 'GPA', 'Expected_Grad'


    matrix = pd.read_csv(matrix_name, sep=',',header=0)

    print(len(matrix)) # rows
    print(len(matrix.columns)) # columns

    # print(data.info())

    # print(data.head)
    # print(data.iloc[:,3])
    # print(data.iloc[:,4])

    # main_matrix.csv data collection
    for cols in range(3,len(matrix.columns),2):
        if (pd.isnull(matrix.iloc[0,cols]) and pd.isnull(matrix.iloc[1,cols + 1])):
            break
        # print(matrix.iloc[0,cols])
        # print(matrix.iloc[1,cols + 1])
        # ------------------------------------------------------------------------------------
        # This loop goes through the applicant name and removes any nickname within parantheses
        name_array = matrix.iloc[0,cols].split()
        applicant_name = ""
        for name in name_array:
            if "(" not in name:
                applicant_name += name + " "
        applicant_name = applicant_name[:len(applicant_name) - 1]
        print(applicant_name)
        # -------------------------------------------------------------------------------------

        interviwers = [matrix.columns[cols], matrix.columns[cols + 1]]
        matrix_percent = [matrix.iloc[len(matrix) - 1, cols ], matrix.iloc[len(matrix) - 1, cols + 1]]
        # index      applicant name     interviewers
        df.loc[len(df.index)] = [applicant_name, semester, interviwers, matrix_percent]
    # ----------------------------------------------------------------------------

    decisions = pd.read_csv(application_name, sep=',',header=0)
    # print(decisions.head())
    # print(decisions.iloc[33,0] + decisions.iloc[33, 1])
    # print(decisions.iloc[1, 1])
    # print(len(decisions))

    print("part 2")

    # add the other desired data columns to the dataframe and initialize to null
    df["GPA"] = np.nan
    df["Round_Decision"] = np.nan
    df["Round_Decision_Quantified"] = np.nan
    df["Notes"] = np.nan
    df["Major"] = np.nan
    df["Minor"] = np.nan
    df["Ethnicity"] = np.nan
    df["Ethnicity_Quantified"] = np.nan
    df["Gender"] = np.nan
    df["Gender_Quantified"] = np.nan
    #df["Recommend"] = [[] for _ in range(len(df))]
    df["Recommend1"] = np.nan
    df["Recommend2"] = np.nan
    df["Recommend1_Quantified"] = np.nan
    df["Recommend2_Quantified"] = np.nan
    df["Grad_Year"] = np.nan

    # for each row in the decisions matrix
    column_names = decisions.columns.values.tolist()
    print(column_names)
    first_name = column_names.index('First Name ')
    last_name = column_names.index('Last Name')
    print(first_name)
    print(last_name)
    for entries in range(0, len(decisions)):
        # if the row is not null
        if not pd.isna(decisions.iloc[entries,0]):
            #print(decisions.iloc[entries,0] + decisions.iloc[entries, 1])
            # set the applicant name for the row to a reference variable used to query the dataframe
            entry_name = decisions.iloc[entries, first_name].strip() + " " + decisions.iloc[entries, last_name].strip()
            # query the dataframe to find the index corresponding to the applicant
            index = df.index[df['Applicant_Name'] == entry_name]
            # for each desired datapoint add the datapoint into the dataframe at the correct index
            df.loc[index, 'GPA'] = decisions.iloc[entries,9]
            df.loc[index, 'Round_Decision'] = decisions.iloc[entries,23]
            if(decisions.iloc[entries,23] == "Reject" or decisions.iloc[entries,23] == "Reject and Reapply"):
                df.loc[index, 'Round_Decision_Quantified'] = 0
            elif(decisions.iloc[entries,23] == "Accept"):
                df.loc[index, 'Round_Decision_Quantified'] = 1
            df.loc[index, 'Notes'] = decisions.iloc[entries,24]
            df.loc[index, 'Major'] = decisions.iloc[entries,5]
            df.loc[index, 'Minor'] = decisions.iloc[entries,6]
            df.loc[index, 'Ethnicity'] = decisions.iloc[entries,12]
            if(decisions.iloc[entries,12] == "I do not wish to disclose."):
                df.loc[index, 'Ethnicity_Quantified'] = 0
            elif(decisions.iloc[entries,12] == "Asian: A person having origins in any of the original peoples of the Far East, Southeast Asia or the Indian Subcontinent, including, for example, Cambodia, China, India, Japan, Korea, Malaysia, Pakistan, the Philippine Islands, Thailand and Vietnam."):
                df.loc[index, 'Ethnicity_Quantified'] = 1
            elif(decisions.iloc[entries,12] == "White: A person having origins in any of the original peoples of Europe, the Middle East or North Africa."):
                df.loc[index, 'Ethnicity_Quantified'] = 2
            elif(decisions.iloc[entries,12] == "Black or African American: A person having origins in any of the black racial groups of Africa."):
                df.loc[index, 'Ethnicity_Quantified'] = 3
            if(decisions.iloc[entries,12] == "Hispanic or Latino: A person of Cuban, Mexican, Puerto Rican, South or Central American, or other Spanish culture or origin regardless of race."):
                df.loc[index, 'Ethnicity_Quantified'] = 4     
            df.loc[index, 'Gender'] = decisions.iloc[entries,13]
            if(decisions.iloc[entries,13] == "I do not wish to disclose."):
                df.loc[index, 'Gender_Quantified'] = 0
            elif(decisions.iloc[entries,13] == "Male"):
                df.loc[index, 'Gender_Quantified'] = 1
            elif(decisions.iloc[entries,13] == "Female"):
                df.loc[index, 'Gender_Quantified'] = 2
            df.loc[index, 'Recommend1'] = decisions.iloc[entries,14]
            if(decisions.iloc[entries,14] == "Do Not Recommend"):
                df.loc[index, 'Recommend1_Quantified'] = 0
            elif(decisions.iloc[entries,14] == "Recommend with Hesitation"):
                df.loc[index, 'Recommend1_Quantified'] = 1
            elif(decisions.iloc[entries,14] == "Recommend"):
                df.loc[index, 'Recommend1_Quantified'] = 2
            elif(decisions.iloc[entries,14] == "Strongly Recommend"):
                df.loc[index, 'Recommend1_Quantified'] = 3
            df.loc[index, 'Recommend2'] = decisions.iloc[entries,15]
            if(decisions.iloc[entries,15] == "Do Not Recommend"):
                df.loc[index, 'Recommend2_Quantified'] = 0
            elif(decisions.iloc[entries,15] == "Recommend with Hesitation"):
                df.loc[index, 'Recommend2_Quantified'] = 1
            elif(decisions.iloc[entries,15] == "Recommend"):
                df.loc[index, 'Recommend2_Quantified'] = 2
            elif(decisions.iloc[entries,15] == "Strongly Recommend"):
                df.loc[index, 'Recommend2_Quantified'] = 3
            df.loc[index, 'Grad_Year'] = decisions.iloc[entries,8]
    

    df.to_csv('complete2.csv', index=False)

fall2022("interview_data/Copy of Behavioral Interview Matrix Fall 2022 - Matrix.csv","interview_data/Copy of Behavioral Interview Matrix Fall 2022 - Decisions.csv", "Fall 2022")



def spring2020(matrix_name, application_name, semester):
    # Dataframe we are putting everything into
    df = pd.DataFrame(columns=['Applicant_Name', 'Semester', 'Interviewers', 'Each_Matrix_Num'])
    #, 'Round_Decision', 'Q1_Feedback', 'Q2_Feedback', 'Q3_Feedback', 'Notes', 'Major', 'Minor', 'Ethnicity', 'Gender', 'Recommend', 'GPA', 'Expected_Grad'


    matrix = pd.read_csv(matrix_name, sep=',',header=0)

    print(len(matrix)) # rows
    print(len(matrix.columns)) # columns

    # print(data.info())

    # print(data.head)
    # print(data.iloc[:,3])
    # print(data.iloc[:,4])

    # main_matrix.csv data collection
    for cols in range(3,len(matrix.columns),2):
        if (pd.isnull(matrix.iloc[0,cols]) and pd.isnull(matrix.iloc[1,cols + 1])):
            break
        # print(matrix.iloc[0,cols])
        # print(matrix.iloc[1,cols + 1])
        # ------------------------------------------------------------------------------------
        # This loop goes through the applicant name and removes any nickname within parantheses
        name_array = matrix.iloc[0,cols].split()
        applicant_name = ""
        for name in name_array:
            if "(" not in name:
                applicant_name += name + " "
        applicant_name = applicant_name[:len(applicant_name) - 1]
        print(applicant_name)
        # -------------------------------------------------------------------------------------

        interviwers = [matrix.columns[cols], matrix.columns[cols + 1]]
        matrix_percent = [matrix.iloc[len(matrix) - 1, cols ], matrix.iloc[len(matrix) - 1, cols + 1]]
        # index      applicant name     interviewers
        df.loc[len(df.index)] = [applicant_name, semester, interviwers, matrix_percent]
    # ----------------------------------------------------------------------------

    decisions = pd.read_csv(application_name, sep=',',header=0)
    # print(decisions.head())
    # print(decisions.iloc[33,0] + decisions.iloc[33, 1])
    # print(decisions.iloc[1, 1])
    # print(len(decisions))

    print("part 2")

    # add the other desired data columns to the dataframe and initialize to null
    df["GPA"] = np.nan
    df["Round_Decision"] = np.nan
    df["Round_Decision_Quantified"] = np.nan
    df["Notes"] = np.nan
    df["Major"] = np.nan
    df["Minor"] = np.nan
    df["Ethnicity"] = np.nan
    df["Ethnicity_Quantified"] = np.nan
    df["Gender"] = np.nan
    df["Gender_Quantified"] = np.nan
    #df["Recommend"] = [[] for _ in range(len(df))]
    df["Recommend1"] = np.nan
    df["Recommend2"] = np.nan
    df["Recommend1_Quantified"] = np.nan
    df["Recommend2_Quantified"] = np.nan
    df["Grad_Year"] = np.nan

    # for each row in the decisions matrix
    column_names = decisions.columns.values.tolist()
    print(column_names)
    first_name = 0
    last_name = column_names.index('Last Name')
    major = column_names.index('Major(s)')
    minor = column_names.index('Minor(s)')
    gpa = column_names.index('Cumulative GPA')
    # gender = column_names.index('What is your gender?')
    # ethnicity = column_names.index('What is your race/ethnicity?')
    # reccomend1 = column_names.index('Recommendation 1')
    # reccomend2 = column_names.index('Recommendation 2')
    # notes = column_names.index('Notes')
    # decision = column_names.index('Decision')
    graduation = column_names.index('Expected Graduation')

    for entries in range(0, len(decisions)):
        # if the row is not null
        if not pd.isna(decisions.iloc[entries,0]):
            #print(decisions.iloc[entries,0] + decisions.iloc[entries, 1])
            # set the applicant name for the row to a reference variable used to query the dataframe
            entry_name = decisions.iloc[entries, first_name].strip() + " " + decisions.iloc[entries, last_name].strip()
            # query the dataframe to find the index corresponding to the applicant
            index = df.index[df['Applicant_Name'] == entry_name]
            # for each desired datapoint add the datapoint into the dataframe at the correct index
            df.loc[index, 'GPA'] = decisions.iloc[entries,gpa]
            # df.loc[index, 'Round_Decision'] = decisions.iloc[entries,decision]
            # if(decisions.iloc[entries,decision] == "Reject" or decisions.iloc[entries,decision] == "Reject and Reapply"):
            #     df.loc[index, 'Round_Decision_Quantified'] = 0
            # elif(decisions.iloc[entries,decision] == "Accept"):
            #     df.loc[index, 'Round_Decision_Quantified'] = 1
            # df.loc[index, 'Notes'] = decisions.iloc[entries,notes]
            df.loc[index, 'Major'] = decisions.iloc[entries,major]
            df.loc[index, 'Minor'] = decisions.iloc[entries,minor]
            # df.loc[index, 'Ethnicity'] = decisions.iloc[entries,ethnicity]
            # if(decisions.iloc[entries,ethnicity] == "I do not wish to disclose."):
            #     df.loc[index, 'Ethnicity_Quantified'] = 0
            # elif(decisions.iloc[entries,ethnicity] == "Asian: A person having origins in any of the original peoples of the Far East, Southeast Asia or the Indian Subcontinent, including, for example, Cambodia, China, India, Japan, Korea, Malaysia, Pakistan, the Philippine Islands, Thailand and Vietnam."):
            #     df.loc[index, 'Ethnicity_Quantified'] = 1
            # elif(decisions.iloc[entries,ethnicity] == "White: A person having origins in any of the original peoples of Europe, the Middle East or North Africa."):
            #     df.loc[index, 'Ethnicity_Quantified'] = 2
            # elif(decisions.iloc[entries,ethnicity] == "Black or African American: A person having origins in any of the black racial groups of Africa."):
            #     df.loc[index, 'Ethnicity_Quantified'] = 3
            # if(decisions.iloc[entries,ethnicity] == "Hispanic or Latino: A person of Cuban, Mexican, Puerto Rican, South or Central American, or other Spanish culture or origin regardless of race."):
            #     df.loc[index, 'Ethnicity_Quantified'] = 4     
            # df.loc[index, 'Gender'] = decisions.iloc[entries,gender]
            # if(decisions.iloc[entries,gender] == "I do not wish to disclose."):
            #     df.loc[index, 'Gender_Quantified'] = 0
            # elif(decisions.iloc[entries,gender] == "Male"):
            #     df.loc[index, 'Gender_Quantified'] = 1
            # elif(decisions.iloc[entries,gender] == "Female"):
            #     df.loc[index, 'Gender_Quantified'] = 2
            # df.loc[index, 'Recommend1'] = decisions.iloc[entries,reccomend1]
            # if(decisions.iloc[entries,reccomend1] == "Do Not Recommend"):
            #     df.loc[index, 'Recommend1_Quantified'] = 0
            # elif(decisions.iloc[entries,reccomend1] == "Recommend with Hesitation"):
            #     df.loc[index, 'Recommend1_Quantified'] = 1
            # elif(decisions.iloc[entries,reccomend1] == "Recommend"):
            #     df.loc[index, 'Recommend1_Quantified'] = 2
            # elif(decisions.iloc[entries,reccomend1] == "Strongly Recommend"):
            #     df.loc[index, 'Recommend1_Quantified'] = 3
            # df.loc[index, 'Recommend2'] = decisions.iloc[entries,reccomend2]
            # if(decisions.iloc[entries,reccomend2] == "Do Not Recommend"):
            #     df.loc[index, 'Recommend2_Quantified'] = 0
            # elif(decisions.iloc[entries,reccomend2] == "Recommend with Hesitation"):
            #     df.loc[index, 'Recommend2_Quantified'] = 1
            # elif(decisions.iloc[entries,reccomend2] == "Recommend"):
            #     df.loc[index, 'Recommend2_Quantified'] = 2
            # elif(decisions.iloc[entries,reccomend2] == "Strongly Recommend"):
            #     df.loc[index, 'Recommend2_Quantified'] = 3
            df.loc[index, 'Grad_Year'] = decisions.iloc[entries,graduation]

    df.to_csv('complete3.csv', index=False)


spring2020("interview_data/Copy of Behavioral Interview Matrix Spring 2020 - Matrix.csv","interview_data/Copy of Behavioral Interview Matrix Spring 2020 - Applications.csv", "Spring 2020")




def spring2021(matrix_name, application_name, semester):
    # Dataframe we are putting everything into
    df = pd.DataFrame(columns=['Applicant_Name', 'Semester', 'Interviewers', 'Each_Matrix_Num'])
    #, 'Round_Decision', 'Q1_Feedback', 'Q2_Feedback', 'Q3_Feedback', 'Notes', 'Major', 'Minor', 'Ethnicity', 'Gender', 'Recommend', 'GPA', 'Expected_Grad'


    matrix = pd.read_csv(matrix_name, sep=',',header=0)

    print(len(matrix)) # rows
    print(len(matrix.columns)) # columns

    # print(data.info())

    # print(data.head)
    # print(data.iloc[:,3])
    # print(data.iloc[:,4])

    # main_matrix.csv data collection
    for cols in range(3,len(matrix.columns),2):
        if (pd.isnull(matrix.iloc[0,cols]) and pd.isnull(matrix.iloc[1,cols + 1])):
            break
        # print(matrix.iloc[0,cols])
        # print(matrix.iloc[1,cols + 1])
        # ------------------------------------------------------------------------------------
        # This loop goes through the applicant name and removes any nickname within parantheses
        name_array = matrix.iloc[0,cols].split()
        applicant_name = ""
        for name in name_array:
            if "(" not in name:
                applicant_name += name + " "
        applicant_name = applicant_name[:len(applicant_name) - 1]
        print(applicant_name)
        # -------------------------------------------------------------------------------------

        interviwers = [matrix.columns[cols], matrix.columns[cols + 1]]
        matrix_percent = [matrix.iloc[len(matrix) - 1, cols ], matrix.iloc[len(matrix) - 1, cols + 1]]
        # index      applicant name     interviewers
        df.loc[len(df.index)] = [applicant_name, semester, interviwers, matrix_percent]
    # ----------------------------------------------------------------------------
    df["GPA"] = np.nan
    df["Round_Decision"] = np.nan
    df["Round_Decision_Quantified"] = np.nan
    df["Notes"] = np.nan
    df["Major"] = np.nan
    df["Minor"] = np.nan
    df["Ethnicity"] = np.nan
    df["Ethnicity_Quantified"] = np.nan
    df["Gender"] = np.nan
    df["Gender_Quantified"] = np.nan
    #df["Recommend"] = [[] for _ in range(len(df))]
    df["Recommend1"] = np.nan
    df["Recommend2"] = np.nan
    df["Recommend1_Quantified"] = np.nan
    df["Recommend2_Quantified"] = np.nan
    df["Grad_Year"] = np.nan


    decisions = pd.read_csv(application_name, sep=',',header=0)

    column_names = decisions.columns.values.tolist()
    first_name = column_names.index('First Name')
    last_name = column_names.index('Last Name')
    major = column_names.index('Major(s)')
    gpa = column_names.index('Cumulative GPA')
    reccomend1 = column_names.index('Recommendation 1')
    reccomend2 = column_names.index('Recommendation 2')
    notes = column_names.index('Notes')
    decision = column_names.index('Decision')
    graduation = column_names.index('Expected Graduation')

    
    for entries in range(0, len(decisions)):
        # if the row is not null
        if not pd.isna(decisions.iloc[entries,0]):
            #print(decisions.iloc[entries,0] + decisions.iloc[entries, 1])
            # set the applicant name for the row to a reference variable used to query the dataframe
            entry_name = decisions.iloc[entries, first_name].strip() + " " + decisions.iloc[entries, last_name].strip()
            print(entry_name)
            # query the dataframe to find the index corresponding to the applicant
            index = df.index[df['Applicant_Name'] == entry_name]
            # for each desired datapoint add the datapoint into the dataframe at the correct index
            df.loc[index, 'GPA'] = decisions.iloc[entries,gpa]
            df.loc[index, 'Round_Decision'] = decisions.iloc[entries,decision]
            if(decisions.iloc[entries,decision] == "Reject" or decisions.iloc[entries,decision] == "Reject and Reapply"):
                df.loc[index, 'Round_Decision_Quantified'] = 0
            elif(decisions.iloc[entries,decision] == "Accept"):
                df.loc[index, 'Round_Decision_Quantified'] = 1
            df.loc[index, 'Notes'] = decisions.iloc[entries,notes]
            df.loc[index, 'Major'] = decisions.iloc[entries,major]
            # df.loc[index, 'Minor'] = decisions.iloc[entries,6]
            # df.loc[index, 'Ethnicity'] = decisions.iloc[entries,12]
            # if(decisions.iloc[entries,12] == "I do not wish to disclose."):
            #     df.loc[index, 'Ethnicity_Quantified'] = 0
            # elif(decisions.iloc[entries,12] == "Asian: A person having origins in any of the original peoples of the Far East, Southeast Asia or the Indian Subcontinent, including, for example, Cambodia, China, India, Japan, Korea, Malaysia, Pakistan, the Philippine Islands, Thailand and Vietnam."):
            #     df.loc[index, 'Ethnicity_Quantified'] = 1
            # elif(decisions.iloc[entries,12] == "White: A person having origins in any of the original peoples of Europe, the Middle East or North Africa."):
            #     df.loc[index, 'Ethnicity_Quantified'] = 2
            # elif(decisions.iloc[entries,12] == "Black or African American: A person having origins in any of the black racial groups of Africa."):
            #     df.loc[index, 'Ethnicity_Quantified'] = 3
            # if(decisions.iloc[entries,12] == "Hispanic or Latino: A person of Cuban, Mexican, Puerto Rican, South or Central American, or other Spanish culture or origin regardless of race."):
            #     df.loc[index, 'Ethnicity_Quantified'] = 4     
            # df.loc[index, 'Gender'] = decisions.iloc[entries,13]
            # if(decisions.iloc[entries,13] == "I do not wish to disclose."):
            #     df.loc[index, 'Gender_Quantified'] = 0
            # elif(decisions.iloc[entries,13] == "Male"):
            #     df.loc[index, 'Gender_Quantified'] = 1
            # elif(decisions.iloc[entries,13] == "Female"):
            #     df.loc[index, 'Gender_Quantified'] = 2
            df.loc[index, 'Recommend1'] = decisions.iloc[entries,reccomend1]
            if(decisions.iloc[entries,reccomend1] == "Do Not Recommend"):
                df.loc[index, 'Recommend1_Quantified'] = 0
            elif(decisions.iloc[entries,reccomend1] == "Recommend with Hesitation"):
                df.loc[index, 'Recommend1_Quantified'] = 1
            elif(decisions.iloc[entries,reccomend1] == "Recommend"):
                df.loc[index, 'Recommend1_Quantified'] = 2
            elif(decisions.iloc[entries,reccomend1] == "Strongly Recommend"):
                df.loc[index, 'Recommend1_Quantified'] = 3
            df.loc[index, 'Recommend2'] = decisions.iloc[entries,reccomend2]
            if(decisions.iloc[entries,reccomend2] == "Do Not Recommend"):
                df.loc[index, 'Recommend2_Quantified'] = 0
            elif(decisions.iloc[entries,reccomend2] == "Recommend with Hesitation"):
                df.loc[index, 'Recommend2_Quantified'] = 1
            elif(decisions.iloc[entries,reccomend2] == "Recommend"):
                df.loc[index, 'Recommend2_Quantified'] = 2
            elif(decisions.iloc[entries,reccomend2] == "Strongly Recommend"):
                df.loc[index, 'Recommend2_Quantified'] = 3
            df.loc[index, 'Grad_Year'] = decisions.iloc[entries,graduation]

    df.to_csv('complete4.csv', index=False)


spring2021("interview_data/Copy of Behavioral Interview Matrix Spring 2021 - Matrix.csv","interview_data/Copy of Behavioral Interview Matrix Spring 2021 - Decisions.csv", "Spring 2021")


def spring2022(matrix_name, application_name, semester):
    # Dataframe we are putting everything into
    df = pd.DataFrame(columns=['Applicant_Name', 'Semester', 'Interviewers', 'Each_Matrix_Num'])
    #, 'Round_Decision', 'Q1_Feedback', 'Q2_Feedback', 'Q3_Feedback', 'Notes', 'Major', 'Minor', 'Ethnicity', 'Gender', 'Recommend', 'GPA', 'Expected_Grad'


    matrix = pd.read_csv(matrix_name, sep=',',header=0)

    print(len(matrix)) # rows
    print(len(matrix.columns)) # columns

    # print(data.info())

    # print(data.head)
    # print(data.iloc[:,3])
    # print(data.iloc[:,4])

    # main_matrix.csv data collection
    for cols in range(3,len(matrix.columns),2):
        if (pd.isnull(matrix.iloc[0,cols]) and pd.isnull(matrix.iloc[1,cols + 1])):
            break
        # print(matrix.iloc[0,cols])
        # print(matrix.iloc[1,cols + 1])
        # ------------------------------------------------------------------------------------
        # This loop goes through the applicant name and removes any nickname within parantheses
        name_array = matrix.iloc[0,cols].split()
        applicant_name = ""
        for name in name_array:
            if "(" not in name:
                applicant_name += name + " "
        applicant_name = applicant_name[:len(applicant_name) - 1]
        print(applicant_name)
        # -------------------------------------------------------------------------------------

        interviwers = [matrix.columns[cols], matrix.columns[cols + 1]]
        matrix_percent = [matrix.iloc[len(matrix) - 1, cols ], matrix.iloc[len(matrix) - 1, cols + 1]]
        # index      applicant name     interviewers
        df.loc[len(df.index)] = [applicant_name, semester, interviwers, matrix_percent]
    # ----------------------------------------------------------------------------
    df["GPA"] = np.nan
    df["Round_Decision"] = np.nan
    df["Round_Decision_Quantified"] = np.nan
    df["Notes"] = np.nan
    df["Major"] = np.nan
    df["Minor"] = np.nan
    df["Ethnicity"] = np.nan
    df["Ethnicity_Quantified"] = np.nan
    df["Gender"] = np.nan
    df["Gender_Quantified"] = np.nan
    #df["Recommend"] = [[] for _ in range(len(df))]
    df["Recommend1"] = np.nan
    df["Recommend2"] = np.nan
    df["Recommend1_Quantified"] = np.nan
    df["Recommend2_Quantified"] = np.nan
    df["Grad_Year"] = np.nan


    decisions = pd.read_csv(application_name, sep=',',header=0)

    column_names = decisions.columns.values.tolist()
    print(column_names)
    first_name = column_names.index('First Name ')
    last_name = column_names.index('Last Name')
    major = column_names.index('Major(s)')
    minor = column_names.index('Minor(s)')
    gpa = column_names.index('Cumulative GPA')
    gender = column_names.index('What is your gender?')
    ethnicity = column_names.index('What is your race/ethnicity?')
    # reccomend1 = column_names.index('Recommendation 1')
    # reccomend2 = column_names.index('Recommendation 2')
    # notes = column_names.index('Notes')
    # decision = column_names.index('Decision')
    graduation = column_names.index('Expected Graduation')

    for entries in range(0, len(decisions)):
        # if the row is not null
        if not pd.isna(decisions.iloc[entries,0]):
            #print(decisions.iloc[entries,0] + decisions.iloc[entries, 1])
            # set the applicant name for the row to a reference variable used to query the dataframe
            entry_name = decisions.iloc[entries, first_name].strip() + " " + decisions.iloc[entries, last_name].strip()
            print(entry_name)
            # query the dataframe to find the index corresponding to the applicant
            index = df.index[df['Applicant_Name'] == entry_name]
            # for each desired datapoint add the datapoint into the dataframe at the correct index
            df.loc[index, 'GPA'] = decisions.iloc[entries,gpa]
            # df.loc[index, 'Round_Decision'] = decisions.iloc[entries,decision]
            # if(decisions.iloc[entries,decision] == "Reject" or decisions.iloc[entries,decision] == "Reject and Reapply"):
            #     df.loc[index, 'Round_Decision_Quantified'] = 0
            # elif(decisions.iloc[entries,decision] == "Accept"):
            #     df.loc[index, 'Round_Decision_Quantified'] = 1
            # df.loc[index, 'Notes'] = decisions.iloc[entries,notes]
            df.loc[index, 'Major'] = decisions.iloc[entries,major]
            df.loc[index, 'Minor'] = decisions.iloc[entries,minor]
            df.loc[index, 'Ethnicity'] = decisions.iloc[entries,ethnicity]
            if(decisions.iloc[entries,ethnicity] == "I do not wish to disclose."):
                df.loc[index, 'Ethnicity_Quantified'] = 0
            elif(decisions.iloc[entries,ethnicity] == "Asian: A person having origins in any of the original peoples of the Far East, Southeast Asia or the Indian Subcontinent, including, for example, Cambodia, China, India, Japan, Korea, Malaysia, Pakistan, the Philippine Islands, Thailand and Vietnam."):
                df.loc[index, 'Ethnicity_Quantified'] = 1
            elif(decisions.iloc[entries,ethnicity] == "White: A person having origins in any of the original peoples of Europe, the Middle East or North Africa."):
                df.loc[index, 'Ethnicity_Quantified'] = 2
            elif(decisions.iloc[entries,ethnicity] == "Black or African American: A person having origins in any of the black racial groups of Africa."):
                df.loc[index, 'Ethnicity_Quantified'] = 3
            if(decisions.iloc[entries,ethnicity] == "Hispanic or Latino: A person of Cuban, Mexican, Puerto Rican, South or Central American, or other Spanish culture or origin regardless of race."):
                df.loc[index, 'Ethnicity_Quantified'] = 4     
            df.loc[index, 'Gender'] = decisions.iloc[entries,gender]
            if(decisions.iloc[entries,gender] == "I do not wish to disclose."):
                df.loc[index, 'Gender_Quantified'] = 0
            elif(decisions.iloc[entries,gender] == "Male"):
                df.loc[index, 'Gender_Quantified'] = 1
            elif(decisions.iloc[entries,gender] == "Female"):
                df.loc[index, 'Gender_Quantified'] = 2
            # df.loc[index, 'Recommend1'] = decisions.iloc[entries,reccomend1]
            # if(decisions.iloc[entries,reccomend1] == "Do Not Recommend"):
            #     df.loc[index, 'Recommend1_Quantified'] = 0
            # elif(decisions.iloc[entries,reccomend1] == "Recommend with Hesitation"):
            #     df.loc[index, 'Recommend1_Quantified'] = 1
            # elif(decisions.iloc[entries,reccomend1] == "Recommend"):
            #     df.loc[index, 'Recommend1_Quantified'] = 2
            # elif(decisions.iloc[entries,reccomend1] == "Strongly Recommend"):
            #     df.loc[index, 'Recommend1_Quantified'] = 3
            # df.loc[index, 'Recommend2'] = decisions.iloc[entries,reccomend2]
            # if(decisions.iloc[entries,reccomend2] == "Do Not Recommend"):
            #     df.loc[index, 'Recommend2_Quantified'] = 0
            # elif(decisions.iloc[entries,reccomend2] == "Recommend with Hesitation"):
            #     df.loc[index, 'Recommend2_Quantified'] = 1
            # elif(decisions.iloc[entries,reccomend2] == "Recommend"):
            #     df.loc[index, 'Recommend2_Quantified'] = 2
            # elif(decisions.iloc[entries,reccomend2] == "Strongly Recommend"):
            #     df.loc[index, 'Recommend2_Quantified'] = 3
            df.loc[index, 'Grad_Year'] = decisions.iloc[entries,graduation]

    df.to_csv('complete5.csv', index=False)


spring2022("interview_data/Copy of Behavioral Interview Matrix Spring 2022 - Matrix.csv","interview_data/Copy of Behavioral Interview Matrix Spring 2022 - Applications.csv", "Spring 2022")


