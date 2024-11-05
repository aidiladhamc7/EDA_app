import streamlit as st
import plotly.express as px
import pandas as pd

# Insert Tittle and markdown
st.title("Exploratory Data Analysis🕵️")
st.markdown("### Univariate Analysis🎯")

# Load the cleaned data from session state
if 'cleaned_data' in st.session_state:
    df = st.session_state['cleaned_data']
    
    # Select a categorical column for analysis
    categorical_column = st.selectbox("Select a categorical column for univariate analysis", df.select_dtypes(include='object').columns)

    # Display class counts and proportions
    categorical_value_counts = df[categorical_column].value_counts()

    categorical_value_proportion = df[categorical_column].value_counts(normalize=True).round(2) * 100

    st.write(f"### Class Counts for {categorical_column}")
    st.write(categorical_value_counts)

    st.write(f"### Class Proportion for {categorical_column} (%)")
    st.write(categorical_value_proportion)

    # Pie Chart for class proportion
    st.write(f"### Pie Chart for {categorical_column}")
    fig_pie = px.pie(
        df,
        names=categorical_column,
        title=f"Proportion of {categorical_column}",
        hole=0.4  # Optional: to create a donut chart
    )
    # Update title font size
    fig_pie.update_layout(
    title={'text': f"Proportion of {categorical_column}", 'font': {'size': 20}},  # Increase title font size
    )

    # Update label font size in pie chart
    fig_pie.update_traces(textinfo='percent+label', textfont_size=15,textfont_color='black')  # Set label font color to black

    st.plotly_chart(fig_pie)

    # Bar Chart for class count
    st.write(f"### Bar Chart for {categorical_column}")
    categorical_value_counts_df = categorical_value_counts.reset_index()
    categorical_value_counts_df.columns = [categorical_column, 'count']  # Rename columns for Plotly
    fig_bar = px.bar(
        categorical_value_counts_df,
        x=categorical_column,
        y='count',
        title=f"Count of {categorical_column} Categories",
        labels={categorical_column: categorical_column, 'count': 'Count'},
        text='count'  # Display count values on top of the bars
    )

    fig_bar.update_layout(
    title={'text': f"Count of {categorical_column} Categories", 'font': {'size': 20}},  # Increase title font size
    )

    fig_bar.update_layout(yaxis={'range': [0, categorical_value_counts.max() * 1.2]})  # Adjust y-axis limit
    # Customize text position and font size for the count labels
    fig_bar.update_traces(textposition='outside', textfont_size=12)  # Position text outside bars and set font size


    st.plotly_chart(fig_bar)

else:
    st.warning("No processed data found. Please go back to the Pre-EDA page to upload and process the data.")
