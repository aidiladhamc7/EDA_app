import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from module.EDA_BE import display_eda_info, round_decimal_columns, check_and_remove_duplicates, check_and_fill_null_values

# Insert Tittle and markdown
st.title("Exploratory Data Analysis🕵️")
st.markdown("### Pre- EDA🎈")

    
def run():
    # Setting up the file uploader widget
    uploaded_files = st.file_uploader("Upload a CSV file here:", type="csv")

    # Check if file has been uploaded. If uploaded, read the file.
    if uploaded_files is not None:
        data = pd.read_csv(uploaded_files)

        # Exclude any column with "ID" in its name
        data = data.loc[:, ~data.columns.str.contains('ID', case=False)]
        # Save the data in the session state
        st.session_state['data'] = data  
        
        # Round numeric columns to 2 decimal places
        st.session_state['data'] = round_decimal_columns(st.session_state['data'])

        # Display basic EDA info
        head_data, shape_info, columns_list, data_types = display_eda_info(st.session_state['data'])

        # Check for null values
        st.write("### Check for Null Values and Fill")
        st.session_state['data'] = check_and_fill_null_values(st.session_state['data'])

        # Check for duplicates and remove them
        st.write("### Check for Duplicates and Remove")
        st.session_state['data'] = check_and_remove_duplicates(st.session_state['data'])
        

        # Download button
        st.write("### Download Cleaned Data")
        
        # Text input for custom file name
        file_name = st.text_input("Enter the desired file name (without .csv):", value="For example: realEstate_cleaned")

        # Add ".csv" if it's not already in the file name
        if not file_name.endswith(".csv"):
            file_name += ".csv"
        
        data_as_csv = st.session_state['data'].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Cleaned Data as CSV",
            data=data_as_csv,
            file_name=file_name,
            mime='text/csv'
        )

        


    else:
        st.write("Please upload a CSV file to proceed.")

if __name__ == "__main__":
    run()