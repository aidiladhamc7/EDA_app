import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Insert Tittle and markdown
st.title("Exploratory Data Analysis🕵️")
st.markdown("### Multivariate Analysis🍖")

# Check if data has been uploaded
if 'data' in st.session_state:
    data = st.session_state['data']
    # Proceed with univariate analysis on 'data'
    col1 = st.selectbox("Select X-axis variable", data.columns)
    col2 = st.selectbox("Select Y-axis variable", data.columns)
    st.write(f"Multivariate Analysis between {col1} and {col2}")

    fig = px.scatter(data, x=col1, y=col2)
    st.plotly_chart(fig)

    
else:
    st.write("No data uploaded yet. Please upload data on the first page.")