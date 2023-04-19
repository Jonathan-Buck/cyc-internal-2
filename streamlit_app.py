#entrypoint for streamlit

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
#raif's imports
import re
import seaborn as sns
import matplotlib.pyplot as plt
# from combine import streamlit_combine

df = pd.read_csv("trial1.csv")
df_ag = pd.read_csv("finals.csv")

final_df = pd.DataFrame(columns=['Applicant_Name', 'Semester', 'Interviewers', 'Each_Matrix_Num', "GPA", "Round_Decision", "Round_Decision_Quantified", "Notes", "Major", "Minor", "Ethnicity", "Ethnicity_Quantified", "Gender", "Gender_Quantified", "Recommend1", "Recommend2", "Recommend1_Quantified", "Recommend2_Quantified", "Grad_Year"])

# bringing in new data from secrets


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

@st.cache_data(ttl=600)
def load_data(sheets_url, gid):
    updated_link = re.sub(r'=.*', '', sheets_url)
    csv_url = updated_link.replace("/edit#gid=", "/export?format=csv&gid=")
    csv_url += gid
    return pd.read_csv(csv_url)

for i in range(len(st.secrets("public_gsheets_url"))):
    matrix_name = load_data(st.secrets("public_gsheets_url")[i], st.secrets("matrix_gid")[i])
    decisions_name = load_data(st.secrets("public_gsheets_url")[i], st.secrets("decisions_gid")[i])
    semester = st.secrets("semester")[i]

    adding_df = streamlit_combine(matrix_name, decisions_name, semester)
    storing_df = pd.concat([final_df, adding_df])

st.write(final_df)

#DATA CLEANING
#In Aggregate, W vs. w in recommend with hesitationc:\Users\srsch\Downloads\Dashboard.ipynb

df.Recommend1 = df.iloc[:, 13].str.replace('w', 'W')
df.Recommend2 = df.iloc[:, 14].str.replace('w', 'W')

df_ag.Recommend1 = df_ag.iloc[:, 14].str.replace('w', 'W')
df_ag.Recommend2 = df_ag.iloc[:, 15].str.replace('w', 'W')

#Goal: Extract Numeric Values from lists
scores1_ = []
scores2_ = []
for l in df ["Each_Matrix_Num"]:
    clean = eval(re.sub(r"[\s%']+", "",l))
    scores1_.append(clean[0])
    scores2_.append(clean[1])

df = df.assign(Score_one=scores1_)
df = df.assign(Score_two=scores2_)


#Creating Difference Variable
diffs = abs(df.Score_one - df.Score_two)
df = df.assign(Score_diff = diffs)

#Goal: Extract Numeric Values from lists in Ag
scores1_ = []
scores2_ = []
for l in df_ag["Each_Matrix_Num"]:
    if 'nan' in l:
        scores1_.append(None)
        scores2_.append(None)
    else:
        clean = eval(re.sub(r"[\s%']+", "",l))
        scores1_.append(clean[0])
        scores2_.append(clean[1])

df_ag = df_ag.assign(Score_one=scores1_)
df_ag = df_ag.assign(Score_two=scores2_)

#Creating Difference Variable
diffs = abs(df_ag.Score_one - df_ag.Score_two)
df_ag = df_ag.assign(Score_diff = diffs)

#THRESHOLDS
# select the two columns you want to append vertically
col1 = df_ag[['Score_one', 'Recommend1']]
col2 = df_ag[['Score_two', 'Recommend2']]

col1 = col1.rename(columns={"Score_one": "Score", "Recommend1": "Recommendation"})
col2 = col2.rename(columns={"Score_two": "Score", "Recommend2": "Recommendation"})


# create a new dataframe by appending the two columns together vertically
appended_scores = pd.concat([col1, col2], axis=0)

# reset the index of the new dataframe
appended_scores = appended_scores.reset_index(drop=True)

# select the two columns you want to append vertically
col1 = df[['Score_one', 'Recommend1']]
col2 = df[['Score_two', 'Recommend2']]

col1 = col1.rename(columns={"Score_one": "Score", "Recommend1": "Recommendation"})
col2 = col2.rename(columns={"Score_two": "Score", "Recommend2": "Recommendation"})


# create a new dataframe by appending the two columns together vertically
appended_scores_single = pd.concat([col1, col2], axis=0)

# reset the index of the new dataframe
appended_scores_single = appended_scores_single.reset_index(drop=True)
#appended_scores_single

# sort the dataframe by category
appended_scores_sorted = appended_scores.sort_values(by=['Recommendation'])

# report descriptive statistics for the 'value' column, grouped by category
stats = appended_scores_sorted.groupby('Recommendation')['Score'].describe()

# sort the dataframe by category
appended_scores_single_sorted = appended_scores_single.sort_values(by=['Recommendation'])

# report descriptive statistics for the 'value' column, grouped by category
stats = appended_scores_single_sorted.groupby('Recommendation')['Score'].describe()

appended_nonzero = appended_scores_single_sorted.replace(0, np.nan)
appended_nonzero = appended_nonzero.dropna(how='all', axis=0)

appended_nonzero2 = appended_scores_sorted.replace(0, np.nan)
appended_nonzero2 = appended_nonzero2.dropna(how='all', axis=0)


#DISCREPANCIES

#Outlier Detection

#Defining New Variable for Discrepancy between Recommendation Decisions
for index, row in df_ag.iterrows():
    if row['Recommend1'] != row['Recommend2']:
        df_ag.at[index, 'Agreement'] = 'Discrepancy'
    else:
        df_ag.at[index, 'Agreement'] = 'No Discrepancy'

for index, row in df.iterrows():
    if row['Recommend1'] != row['Recommend2']:
        df.at[index, 'Agreement'] = 'Discrepancy'
    else:
        df.at[index, 'Agreement'] = 'No Discrepancy'

#Creating outlier and flag values      
df_ag_flag = df_ag[df_ag['Score_diff']> 10].copy()
df_ag_outlier = df_ag[df_ag['Score_diff'] > 30].copy()

df_flag = df[df['Score_diff']> 10].copy()
df_outlier = df[df['Score_diff'] > 30].copy()

#Look into Abisha Finn for max






st.title("CYC Internal Analytics Dashboard")





st.header("Threshold Insights")


thresh1 = sns.displot(appended_nonzero, x="Score", hue="Recommendation", kind="ecdf")
st.pyplot(thresh1)

thresh2 = sns.displot(appended_nonzero2, x="Score", hue="Recommendation", kind="ecdf")
st.pyplot(thresh2)



st.header("Discrepancy Analysis")

st.write("Flagged interviews")
st.write(df_flag)

st.write("Aggregate flagged interviews")
st.write(df_ag_flag)


fig, axes = plt.subplots(2, 2, figsize=(20, 10))
fig.suptitle('Score Differences and Discrepancies')

#Fall 2022
sns.kdeplot(ax=axes[0,0], data=df, x="Score_diff", hue="Agreement")
axes[0,0].set_title('Fall 2022')

#Fall 2022 Flagged
sns.kdeplot(ax=axes[0,1], data=df_flag, x="Score_diff", hue="Agreement")
axes[0,1].set_title('Fall 2022 Flagged')

#Aggregate
sns.kdeplot(ax=axes[1,0], data=df_ag, x="Score_diff", hue="Agreement")
axes[1,0].set_title('Aggregate')

#Aggregate Flagged
sns.kdeplot(ax=axes[1,1], data=df_ag_flag, x="Score_diff", hue="Agreement")
axes[1,1].set_title('Aggregate Flagged')

st.write(fig)




st.header("Impact of GPA")


st.header("Demographics")

unknown = 0
white = 0
black = 0
asian = 0
hispanic = 0

for entries in range(0, len(df_ag)):
    if(df_ag.iloc[entries,10] == "I do not wish to disclose."):
        unknown += 1
    elif(df_ag.iloc[entries,10] == "Asian: A person having origins in any of the original peoples of the Far East, Southeast Asia or the Indian Subcontinent, including, for example, Cambodia, China, India, Japan, Korea, Malaysia, Pakistan, the Philippine Islands, Thailand and Vietnam."):
        asian += 1
    elif(df_ag.iloc[entries,10] == "White: A person having origins in any of the original peoples of Europe, the Middle East or North Africa."):
        white += 1
    elif(df_ag.iloc[entries,10] == "Black or African American: A person having origins in any of the black racial groups of Africa."):
        black += 1
    elif(df_ag.iloc[entries,10] == "Hispanic or Latino: A person of Cuban, Mexican, Puerto Rican, South or Central American, or other Spanish culture or origin regardless of race."):
        hispanic += 1


pie = px.pie(values=[unknown, white, black, asian, hispanic], names=['Prefer not to disclose','White', 'Black', 'Asian', 'Hispanic'], title='Historical Demographic Breakdown of Applicants')
st.plotly_chart(pie)

st.header("Appendix")
st.subheader("Historical Aggregate Data")
st.write(df_ag)