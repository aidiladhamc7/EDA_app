#1 Import Package
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Insert Tittle and markdown
st.title("Exploratory Data Analysis🕵️")
st.markdown("### Univariate Analysis🎪")

# Check if data has been uploaded
if 'data' in st.session_state:
    data = st.session_state['data']
    # Proceed with univariate analysis on 'data'



    
else:
    st.write("No data uploaded yet. Please upload data on the first page.")
