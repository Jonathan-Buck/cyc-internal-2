#entrypoint for streamlit

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.title("CYC Internal Analytics Dashboard")


df = pd.read_csv("finals.csv")


st.header("Threshold Insights")


st.header("Discrepancy Analysis")


st.header("Impact of GPA")


st.header("Demographics")

unknown = 0
white = 0
black = 0
asian = 0
hispanic = 0

for entries in range(0, len(df)):
    if(df.iloc[entries,10] == "I do not wish to disclose."):
        unknown += 1
    elif(df.iloc[entries,10] == "Asian: A person having origins in any of the original peoples of the Far East, Southeast Asia or the Indian Subcontinent, including, for example, Cambodia, China, India, Japan, Korea, Malaysia, Pakistan, the Philippine Islands, Thailand and Vietnam."):
        asian += 1
    elif(df.iloc[entries,10] == "White: A person having origins in any of the original peoples of Europe, the Middle East or North Africa."):
        white += 1
    elif(df.iloc[entries,10] == "Black or African American: A person having origins in any of the black racial groups of Africa."):
        black += 1
    elif(df.iloc[entries,10] == "Hispanic or Latino: A person of Cuban, Mexican, Puerto Rican, South or Central American, or other Spanish culture or origin regardless of race."):
        hispanic += 1


pie = px.pie(values=[unknown, white, black, asian, hispanic], names=['Prefer not to disclose','White', 'Black', 'Asian', 'Hispanic'], title='Historical Demographic Breakdown of Applicants')
st.plotly_chart(pie)

st.header("Appendix")
st.subheader("Historical Aggregate Data")
st.write(df)