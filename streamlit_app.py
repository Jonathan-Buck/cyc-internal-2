#entrypoint for streamlit

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.title("CYC Internal Analytics Dashboard")


df = pd.read_csv("finals.csv")

print(df)

st.header("Testing Datasets")
st.subheader("Dataframes")
st.write("We can display a dataframe that can be manipulated and viewed in the dashboard:")
st.write(df)