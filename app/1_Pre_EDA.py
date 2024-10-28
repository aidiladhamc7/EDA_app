import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from module.EDA_BE import display_eda_info, round_decimal_columns, check_and_remove_duplicates, check_and_fill_null_values

# Insert Tittle and markdown
st.title("Exploratory Data Analysis🕵️")
st.markdown("### Pre- EDA🎈")

# Setting up the file uploader widget
uploaded_files = st.file_uploader("Upload a CSV file here:", type="csv")

# Check if file has been uploaded. If uploaded, read the file.
if uploaded_files is not None:
    raw_data = pd.read_csv(uploaded_files)
    
    # Exclude any column with "ID" in its name
    data = raw_data.loc[:, ~raw_data.columns.str.contains('ID', case=False)]
    
    # Round numeric columns to 2 decimal places
    rounded_data = round_decimal_columns(data)

    # Display basic EDA info
    head_data, shape_info, columns_list, data_types = display_eda_info(data)

    # Check for duplicates and remove them
    st.write("### Check for Duplicates and Remove")
    Remove_Duplicated = check_and_remove_duplicates(data)
      
   # Check for null values
    st.write("### Check for Null Values and Fill")
    Fill_Null = check_and_fill_null_values(data)

    # Seperate object and numeric columns
    obj = [col for col in data.columns if data[col].dtype == 'object']
    int_float = [col for col in data.columns if data[col].dtype in ['int64', 'float64']]  

                                                                                                                                                                    

    # Insert Remove Null Values button to remove values and replace with mean & mode
    # Adding submit button sidebar
    with st.form(key='my_form'):
        with st.sidebar:
            st.sidebar.header("To Remove Null Values, press button below")
            submit_button = st.form_submit_button(label="Remove Null")

    # Replace null values with mean and mode
    if submit_button:
        for col in data.columns:
            if data[col].dtype == 'object':
                data[col].fillna(data[col].mode()[0], inplace=True)
            else:
                data[col].fillna(data[col].mean(), inplace=True)

    # Find number of null values in each column
    null_counts = data.isnull().sum().tolist()

    # If number of null values is 0 it will display some text, else it will display bar plot by each column
    if max(null_counts) == 0:
        st.write('Total number of null values in dataset is: 0')
    else:
        st.write("Bar plot to know number of null values in each column")
        st.write("Total number of null values in dataset is: "+ str(max(null_counts)))
        fig2 =px.bar(x=data.columns, y=null_counts, labels={'x': "Column Names", 'y': "Number of Null Values"})
        st.plotly_chart(fig2)

    # Frequency Plot for categorical variables
    st.sidebar.header("Select Variable")
    selected_pos = st.sidebar.selectbox('Object Variable',obj)
    st.write("Bar chart to know frequency of each category")
    #frequency_data = data[selected_pos].value_counts()
    #st.write(frequency_data.index)

    # Convert frequency_data to a DataFrame and rename columns
    if selected_pos:
        frequency_data = data[selected_pos].value_counts().reset_index()
        frequency_data.columns = [selected_pos, 'count']  # Rename columns to match labels

        # Create the plot
        fig = px.bar(frequency_data, x=selected_pos, y='count', labels={'x': selected_pos, 'y': 'count'},
                     color=frequency_data[selected_pos],  # Set color by category
                     color_discrete_sequence=px.colors.qualitative.Plotly)  # Choose a colorful palette
        st.plotly_chart(fig)

    # Histogram for numeric variables
    st.sidebar.header('Select Numeric Variable')
    selected_pos1 = st.sidebar.selectbox('Int or Float Variables', int_float)
    st.write("Bar plot to show count of values based on range")

    # Calculate the step size and ensure it's at least 1
    if selected_pos1:
        step_size = max(1, int(max(data[selected_pos1]) / 10))
        counts, bins = np.histogram(data[selected_pos1], bins=range(int(min(data[selected_pos1])), int(max(data[selected_pos1])), step_size))
        bins = 0.5 * (bins[:-1] + bins[1:])
        
        fig1 = px.bar(x=bins, y=counts, labels={'x': selected_pos1, 'y': 'count'},
               color=counts,  # Set color by count values for each bin
               color_discrete_sequence=px.colors.qualitative.Plotly)
        st.plotly_chart(fig1)

    # Correlation Chart
    st.sidebar.header('Select Variable for Correlation')
    selected_pos2 = st.sidebar.multiselect('Int or Float Variables - Correlation', int_float)
    st.write("Scatter plot for correlation")

    if len(selected_pos2) == 2:
        fig3 = px.scatter(data, x=selected_pos2[0], y=selected_pos2[1])
        st.plotly_chart(fig3)
    else: 
        st.write("Select only 2 variables")

else:
    st.write("Please upload a CSV file to proceed.")