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


st.header("Appendix")
st.subheader("Historical Aggregate Data")
st.write(df)