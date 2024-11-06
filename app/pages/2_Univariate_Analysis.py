import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Insert Tittle and markdown
st.title("Exploratory Data Analysis🕵️")
st.subheader("Univariate Analysis🎯")

st.markdown("### 1. Univariate Analysis for Numerical Variables")
# Load the cleaned data from session state
if 'cleaned_data' in st.session_state:
    df = st.session_state['cleaned_data']
       
    # Select a numeric column for univariate analysis
    numeric_column = st.selectbox("Select a numeric column for univariate analysis", df.select_dtypes(include=np.number).columns)
    
    # A. Shape of Distribution
    st.markdown("#### A. Shape of Distribution for: " + numeric_column)
    st.write(f"#### Histogram of {numeric_column}")
    mean = df[numeric_column].mean().round(2)
    median = df[numeric_column].median().round(2)
    
    # Plot Histogram with Mean and Median Lines
    fig_hist = px.histogram(df, x=numeric_column, nbins=22, title=f"Histogram of {numeric_column}")
    fig_hist.add_vline(x=mean, line_dash="dash", line_color="red", annotation_text="Mean", annotation_position="top left")
    fig_hist.add_vline(x=median, line_dash="dot", line_color="green", annotation_text="Median", annotation_position="top right")
    fig_hist.update_traces(marker_line_color='black', marker_line_width=1)  # Outline for histogram bars
    st.plotly_chart(fig_hist)

    # Additional Shape Information: Skewness and Kurtosis
    st.write("#### Shape Analysis")
    skewness = df[numeric_column].skew()
    st.write(f"Skewness: {skewness}")

    # Generate hypothesis based on skewness
    if skewness > 0:
        hypothesis = f"Hypothesis: More occurrences of lower {numeric_column} values compared to higher {numeric_column} values."
    elif skewness < 0:
        hypothesis = f"Hypothesis: More occurrences of higher {numeric_column} values compared to lower {numeric_column} values."
    else:
        hypothesis = f"Hypothesis: The distribution of {numeric_column} values is approximately symmetric, with similar frequencies across value ranges."       

    st.write(hypothesis)
  
  
    # B. Measures of Central Tendency
    st.markdown("####")
    st.markdown("#### B. Measures of Central Tendency for: " + numeric_column)
    st.write(f"#### Summary Statistics for {numeric_column}")
    st.write(df[numeric_column].describe().round(2))  # Display summary table
    
    # Display Mean, Median, and Mode
    mode = df[numeric_column].mode().values[0] if not df[numeric_column].mode().empty else "No mode"
    st.write(f"Mean: {mean}")
    st.write(f"Median: {median}")
    st.write(f"Mode: {mode}")

    # C. Measures of Dispersion
    st.markdown("####")
    st.write("### C. Measures of Dispersion for: " + numeric_column)
    st.write(f"Standard Deviation: {df[numeric_column].std().round(2)}")
    st.write(f"Variance: {df[numeric_column].var().round(2)}")
    #st.write(f"Range: {(df[numeric_column].max() - df[numeric_column].min()).round(2)}")
    
    # Interquartile Range (IQR)
    Q1 = df[numeric_column].quantile(0.25).round(2)
    Q3 = df[numeric_column].quantile(0.75).round(2)
    IQR = (Q3 - Q1).round(2)
    #st.write(f"IQR (Interquartile Range): {IQR}")

    # D. Quartile Range and Outlier Analysis
    st.markdown("####")
    st.markdown("### D. Quartile Range and Outlier Analysis for: " + numeric_column)
    
    # Box Plot for Outlier Visualization
    st.write(f"### Box Plot of {numeric_column}")
    fig_box = px.box(df, y=numeric_column, title=f"Box Plot of {numeric_column}")
    st.plotly_chart(fig_box)

    # Outlier Detection using IQR Method
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[numeric_column] < lower_bound) | (df[numeric_column] > upper_bound)][numeric_column]
    st.write(f"Number of outliers: {len(outliers)}")
    st.write(outliers)

    # E. Conclusion/Interpretation
    st.markdown("####")
    st.write("### E. Conclusion/Interpretation for: " + numeric_column)
     # Calculate summary statistics
    median = df[numeric_column].median().round(2)
    Q1 = df[numeric_column].quantile(0.25).round(2)
    Q3 = df[numeric_column].quantile(0.75).round(2)
    skewness = df[numeric_column].skew().round(2)

    # Generate a dynamic conclusion summary
    if skewness > 0:
        skew_text = f"{numeric_column} is skewed to the right (positive skew), meaning more occurrences of lower {numeric_column} values."
    elif skewness < 0:
        skew_text = f"{numeric_column} is skewed to the left (negative skew), indicating more occurrences of higher {numeric_column} values."
    else:
        skew_text = f"{numeric_column} is approximately symmetric, with similar frequencies across value ranges."

    # Create a summary text
    summary = f"""
    #### Summary of {numeric_column} distribution
    - Median is located at {median}. {skew_text}
    - 25% of observations have {numeric_column} values less than {Q1}.
    - 25% of observations have {numeric_column} values more than {Q3}.
    - 50% of observations have {numeric_column} values between {Q1} and {Q3}.
    - Half of the observations have {numeric_column} values more than {median}.
    """
    # Display the summary
    st.markdown(summary)

   # Univariate Analysis for Categorical Analysis
    st.markdown("#") # Create space between Categorical Analysis and Numerical Analysis
    st.markdown("#### 2. Univariate Analysis for Categorical Variables")
    # Select a categorical column for analysis
    categorical_column = st.selectbox("Select a categorical column for univariate analysis", df.select_dtypes(include='object').columns)

    # Display class counts and proportions
    categorical_value_counts = df[categorical_column].value_counts()

    categorical_value_proportion = (df[categorical_column].value_counts(normalize=True) * 100).round(0)

    st.write(f"### Class Counts for: {categorical_column}")
    st.write(categorical_value_counts)

    st.write(f"### Class Proportion for: {categorical_column} (%)")
    st.write(categorical_value_proportion)

    # Create a new DataFrame with categories and their rounded percentages
    proportion_df = pd.DataFrame({
        categorical_column: categorical_value_counts.index,
        'Proportion': categorical_value_proportion.values
    })

    # Pie Chart for class proportion
    st.write(f"### Pie Chart for {categorical_column}")
    fig_pie = px.pie(
        proportion_df,
        names=categorical_column,
        values='Proportion',
        title=f"Proportion of {categorical_column}",
        hole=0.4  # Optional: to create a donut chart
    )

    # Update title font size
    fig_pie.update_layout(
    title={'text': f"Proportion of {categorical_column}", 'font': {'size': 20}},  # Increase title font size
    )

    # Update label font size in pie chart
    fig_pie.update_traces(textinfo='label+value', textfont_size=15, texttemplate='%{label}:<br>%{value}%')

    st.plotly_chart(fig_pie)

    # Bar Chart for class count
    st.write(f"### Bar Chart for: {categorical_column}")
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
