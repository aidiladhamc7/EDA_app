import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Insert Tittle and markdown
st.title("Exploratory Data Analysis🕵️")
st.markdown("### Pre- EDA🎈")

# Setting up the file uploader widget
uploaded_files = st.file_uploader("Upload a CSV file here:", type="csv")

# Check if file has been uploaded. If uploaded, read the file.
if uploaded_files is not None:
    data = pd.read_csv(uploaded_files)
    obj = []
    int_float = []
    for i in data.columns:
        clas = data[i].dtypes
        if clas == 'object':
            obj.append(i)
        else:
            int_float.append(i)

# Insert Remove Null Values button to remove values and replace with mean & mode
# Adding submit button sidebar
with st.form(key='my_form'):
    with st.sidebar:
        st.sidebar.header("To Remove Null Values, press button below")
        submit_button = st.form_submit_button(label="remove Null")

# Replace null value with mean and mode
if submit_button:
    for i in data.columns:
        clas = data[i].dtypes
        if clas == 'object':
            data[i].fillna(data[i].mode()[0], inplace=True)
        else:
            data[i].fillna(data[i].mean(), inplace=True)

# Find number of null values in each column
lis = []
for i in data.columns:
    dd = sum(pd.isnull(data[i]))
    lis.append(dd)

# If number of null values is 0 it will display some text, else it will display bar plot by each column
if max(lis) == 0:
    st.write('Total number of null values in dataset is: '+ str(max(lis)))
else:
    st.write("Bar plot to know number of null values in each column")
    st.write("Total number of null values in dataset is: "+ str(max(lis)))
    fig2 =px.bar(x=data.columns, y=lis, labels={'x': "Column Names", 'y': "Number of Null Values"})
    st.plotly_chart(fig2)

# Frequency Plot
st.sidebar.header("Select Variable")
selected_pos = st.sidebar.selectbox('Object Variable',obj)
st.write("Bar chart to know frequency of each ctegory")
frequency_data = data[selected_pos].value_counts()
st.write(frequency_data.index)

# Convert frequency_data to a DataFrame and rename columns
frequency_data = frequency_data.reset_index()
frequency_data.columns = [selected_pos, 'count']  # Rename columns to match labels

# Create the plot
fig = px.bar(frequency_data, x=selected_pos, y='count', labels={'x': selected_pos, 'y': 'count'})
st.plotly_chart(fig)

# Histogram
st.sidebar.header('Select Variable')
selected_pos1 = st.sidebar.selectbox('Int or Float Variables', int_float)
st.write("Bar plot to know count of values based on range")

# Calculate the step size and ensure it's at least 1
step_size = max(1, int(max(data[selected_pos1]) / 10))
# Use the calculated step_size in the range function
counts, bins = np.histogram(data[selected_pos1], bins=range(int(min(data[selected_pos1])), int(max(data[selected_pos1])), step_size))
bins = 0.5 * (bins[:-1] + bins[1:])
fig1 = px.bar(x=bins, y=counts, labels={'x': selected_pos1, 'y': 'count'})
st.plotly_chart(fig1)
