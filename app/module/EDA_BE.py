import pandas as pd
import streamlit as st

def display_eda_info(data):
    """Function to display basic EDA info."""
    # First 10 rows
    st.write("### First 5 rows of the data")
    st.dataframe(data.head(5))
    head_data = data.head(5)
    
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

def round_decimal_columns(data):
    for col in data.select_dtypes(include=['float64']).columns:
        data[col] = data[col].round(2)
    return data

import streamlit as st

def check_and_remove_duplicates(data):
    # Check for duplicates
    duplicated_rows = data[data.duplicated(keep=False)]
    
    if not duplicated_rows.empty:
        # Display duplicated rows
        st.write("Duplicated Rows Found:")
        st.dataframe(duplicated_rows)
        
        # Show the "Remove Duplicates" button if duplicates are found
        if st.button("Remove Duplicates"):
            data.drop_duplicates(keep='first', inplace=True)
            st.write("Duplicated rows have been removed.😁")
            
            # Display new shape of data
            st.write("#### New Total Number of Rows and Columns:")
            st.write(f"Rows: {data.shape[0]}, Columns: {data.shape[1]}")

    else:
        # If no duplicates are found
        st.write("No duplicated rows found.")

    return data    

def check_and_fill_null_values(data):
    # Check if data is valid (not None)
    if data is None:
        st.write("Error: No data to check for null values.")
        return None  # Return None if no data is present
    
    # Check for null values
    null_counts = data.isnull().sum()
    
    # Display null counts
    if null_counts.sum() == 0:
        st.write("No null values found in the dataset.")
    else:
        st.write("Null values found in the following columns:")
        st.write(null_counts[null_counts > 0])
        
        # Show the button to fill null values if any are present
        if st.button("Fill Null Values"):
            for col in data.columns:
                if data[col].dtype == 'object':  # Categorical columns
                    data[col] = data[col].fillna(data[col].mode()[0])
                else:  # Numeric columns
                    data[col] = data[col].fillna(data[col].mean())
            st.write("Null values have been filled.")
            
            # Display the new null count for verification
            st.write("### Null Values After Filling")
            st.write(data.isnull().sum())

            st.write(f"Rows: {data.shape[0]}, Columns: {data.shape[1]}")
    
    return data

