import pandas as pd
import numpy as np




secrets = [[]]


# pass in the read csv files from the respective links into the function and semester
def streamlit_combine(matrix_name, decisions_name, semester):
    # Dataframe we are putting everything into
    df = pd.DataFrame(columns=['Applicant_Name', 'Semester', 'Interviewers', 'Each_Matrix_Num'])
    #, 'Round_Decision', 'Q1_Feedback', 'Q2_Feedback', 'Q3_Feedback', 'Notes', 'Major', 'Minor', 'Ethnicity', 'Gender', 'Recommend', 'GPA', 'Expected_Grad'


    matrix = matrix_name

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

    decisions = decisions_name
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
    

    return df



# final_df = pd.DataFrame(columns=['Applicant_Name', 'Semester', 'Interviewers', 'Each_Matrix_Num', "GPA", "Round_Decision", "Round_Decision_Quantified", "Notes", "Major", "Minor", "Ethnicity", "Ethnicity_Quantified", "Gender", "Gender_Quantified", "Recommend1", "Recommend2", "Recommend1_Quantified", "Recommend2_Quantified", "Grad_Year"])

# st.secrets
# for items in list_matrix:
#     matrix_stored = items[0]
#     decisions_stored = items[1]
#     semester = items[1]

#     read_matrix_csv = pd.read_csv(matrix_stored, sep=',',header=0)

#     read_decisions_csv = pd.read_csv(decisions_stored, sep=',',header=0)

#     adding_df = streamlit_combine(read_matrix_csv, read_decisions_csv, semester)


#     storing_df = pd.concat([final_df, adding_df])

