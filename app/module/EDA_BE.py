import pandas as pd
import streamlit as st

def display_eda_info(data):
    """Function to display basic EDA info."""
    # First 10 rows
    st.write("### First 10 rows of the data")
    st.dataframe(data.head(10))
    head_data = data.head(10)
    
    # Number of rows and columns
    st.write("### Total Number of Rows and Columns")
    st.write(f"Rows: {data.shape[0]}, Columns: {data.shape[1]}")  # data.shape gives (rows, columns)
    shape_info = (data.shape[0], data.shape[1])
    
    # Column names
    st.write("### Column Names")
    st.write(data.columns.tolist())
    columns_list = data.columns.tolist()
    
    # Data types
    st.write("### Data Types for Each Column")
    st.write(data.dtypes)
    data_types = data.dtypes
    
    return head_data, shape_info, columns_list, data_types