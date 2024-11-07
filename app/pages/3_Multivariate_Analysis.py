import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import scipy.stats as stats

# Insert Tittle and markdown
st.title("Exploratory Data Analysis🕵️")
st.header("Multivariate Analysis🎠")

# Load the data from session state
if 'cleaned_data' in st.session_state:
    df = st.session_state['cleaned_data']

    ## 1. Analysis of Continuous (Numeric) vs Numeric Variable
    st.subheader("1. Analysis of Continuous (Numeric) vs Numeric Variable")

    # Select response and feature variables
    response_var = st.selectbox("Select response variable (Y-axis)", df.select_dtypes(include=[np.number]).columns)
    feature_var = st.selectbox("Select feature variable (X-axis)", df.select_dtypes(include=[np.number]).columns)
    
    if response_var and feature_var:
        # Scatter plot
        st.subheader(f"i) Scatter Plot of {response_var} vs. {feature_var}")
        fig_scatter = px.scatter(df, x=feature_var, y=response_var, title=f"{response_var} vs. {feature_var}")
        st.plotly_chart(fig_scatter)

        # Generate dynamic findings
        st.write("**Finding:**")
        # Calculate correlation coefficient
        correlation = df[response_var].corr(df[feature_var])

        # Direction of the relationship
        if correlation > 0:
            st.write(f"- {response_var} increases when {feature_var} increases.")
        elif correlation < 0:
            st.write(f"- {response_var} decreases when {feature_var} increases.")
        else:
            st.write(f"- There is no clear linear relationship between {response_var} and {feature_var}.")

        # Additional findings on trend direction and clarity
        if correlation > 0:
            relationship_type = "Positive linear relationship"
        elif correlation < 0:
            relationship_type = "Negative linear relationship"
        else:
            relationship_type = "No linear relationship"

        if abs(correlation) >= 0.7:
            trend_clarity = "Trend is clear"
        elif 0.4 <= abs(correlation) < 0.7:
            trend_clarity = "Trend is moderately clear"
        else:
            trend_clarity = "Trend is unclear"

        # Display additional findings
        st.write(f"- {relationship_type}")
        st.write(f"- {trend_clarity}")


        # Correlation coefficient
        st.subheader("ii) Correlation Coefficient")
        corr = df[[feature_var, response_var]].corr().iloc[0, 1]
        st.write(f"Correlation between {response_var} and {feature_var}: {corr}")
        
        # Generate dynamic finding based on correlation strength and direction
        st.write("**Finding:**")

        # Determine the strength of the correlation
        if abs(corr) >= 0.7:
            strength = "strong"
        elif 0.4 <= abs(corr) < 0.7:
            strength = "moderate"
        else:
            strength = "weak"

        # Determine the direction of the correlation
        if corr > 0:
            direction = "positive"
            relationship_statement = f"The higher the {feature_var}, the higher the {response_var}."
        elif corr < 0:
            direction = "negative"
            relationship_statement = f"The higher the {feature_var}, the lower the {response_var}."
        else:
            direction = "no clear linear"

        # Print finding based on the calculated values
        if corr != 0:
            st.write(f"- A correlation coefficient of {corr} (close to {'+1' if corr > 0 else '-1'}) indicates a {strength} {direction} relationship between {response_var} and {feature_var}.")
            st.write(f"- {relationship_statement}")
        else:
            st.write(f"- There is no clear linear relationship between {response_var} and {feature_var}.")


        # Heatmap for correlation matrix
        st.subheader("iii) Correlation Matrix (Heatmap)")
        numeric_df = df.select_dtypes(include=[np.number])  # Select only numeric columns
        correlation_matrix = numeric_df.corr()  # Compute correlation matrix on numeric data
        fig_heatmap = px.imshow(correlation_matrix, text_auto=True, title="Correlation Matrix Heatmap", color_continuous_scale='RdBu_r')
        st.plotly_chart(fig_heatmap)

        # Generate findings based on the correlation matrix
        st.write("**Finding:**")

        # Define a threshold for identifying strong correlations
        threshold = 0.7  # Adjust as needed for defining 'strong' correlation

        # Find strong correlations in the matrix
        strong_corr_pairs = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i + 1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) >= threshold:
                    strong_corr_pairs.append((correlation_matrix.columns[i], correlation_matrix.columns[j], corr_value))

        # Display findings for each strong correlation
        if strong_corr_pairs:
            for col1, col2, corr_value in strong_corr_pairs:
                color_intensity = "cool-colored (blue)" if corr_value > 0 else "warm-colored (red)"
                relationship = "positive" if corr_value > 0 else "negative"
                st.write(f"- High color intensity towards {color_intensity} indicates a {relationship} correlation ({corr_value:.2f}) between {col1} and {col2}.")
        else:
            st.write("- No strong correlations found with high color intensity.")


    ## 2. Analysis of Continuous (Numeric) vs Categorical Variable
    st.subheader("2. Analysis of Continuous (Numeric) vs Categorical Variable")

    # Select numeric variable and categorical variable
    numeric_var = st.selectbox("Select numeric variable", df.select_dtypes(include=[np.number]).columns, key='numeric_var')
    categorical_var = st.selectbox("Select categorical variable", df.select_dtypes(include=['object']).columns)

    if numeric_var and categorical_var:
        # Group by and mean comparison
        st.subheader(f"i) Comparing Mean of {numeric_var} Across {categorical_var}")
        mean_comparison = df.groupby(categorical_var)[numeric_var].mean().round(2).reset_index()
        mean_comparison = mean_comparison.sort_values(by=numeric_var, ascending=False).reset_index(drop=True)  # Sort by mean in descending order
        st.write(mean_comparison)

        # Generate dynamic finding
        st.write("**Finding:**")

        # Check if there are at least two categories to compare
        if len(mean_comparison) >= 2:
            highest_category = mean_comparison.iloc[0][categorical_var]
            highest_mean = mean_comparison.iloc[0][numeric_var]
            lowest_category = mean_comparison.iloc[-1][categorical_var]
            lowest_mean = mean_comparison.iloc[-1][numeric_var]

            st.write(f"- The mean {numeric_var} of {highest_category} is the highest at {highest_mean} and the lowest is {lowest_category} at {lowest_mean}.")
            st.write(f"- This suggests that {numeric_var} may be affected by {categorical_var}, but further analysis is needed for clarification.")
        else:
            st.write(f"- Not enough categories in {categorical_var} to provide a meaningful comparison.")
        
        # Box plot to visualize variation
        st.subheader(f"ii) Box Plot of {numeric_var} by {categorical_var}")
        fig_box = px.box(df, x=categorical_var, y=numeric_var, title=f"{numeric_var} Distribution by {categorical_var}")
        st.plotly_chart(fig_box)

        # ANOVA test for mean difference
        st.subheader(f"iii) ANOVA Test: Significance of {numeric_var} Across {categorical_var}")
        unique_groups = df[categorical_var].unique()
        group_data = [df[df[categorical_var] == group][numeric_var] for group in unique_groups]
        anova_result = stats.f_oneway(*group_data)
        st.write(f"ANOVA test result: F = {anova_result.statistic:.2f}, p-value = {anova_result.pvalue:.3f}")
        st.write("Significant difference across groups." if anova_result.pvalue < 0.05 else "No significant difference across groups.")

        # Generate dynamic finding based on ANOVA result
        st.write("**Finding:**")

        if anova_result.pvalue < 0.05:
            st.write(f"- The p-value of the ANOVA test is {anova_result.pvalue:.3f}, which is < 0.05.")
            st.write(f"- This suggests that the mean {categorical_var} for {numeric_var} is significantly different.")
            st.write(f"- Therefore, {categorical_var} appears to be affected by {numeric_var}.")
        else:
            st.write(f"- The p-value of the ANOVA test is {anova_result.pvalue:.3f}, which is > 0.05.")
            st.write(f"- This suggests that there is no significant difference in the mean {categorical_var} across different values of {numeric_var}.")
            st.write(f"- Therefore, {categorical_var} not affected by {numeric_var}.")

    ## 3. Analysis of Categorical vs Categorical Variable
    st.header("3. Analysis of Categorical vs Categorical Variable")

    # Select two categorical variables
    cat_var1 = st.selectbox("Select first categorical variable", df.select_dtypes(include=['object']).columns, key='cat_var1')
    cat_var2 = st.selectbox("Select second categorical variable (response_variable)", df.select_dtypes(include=['object']).columns, key='cat_var2')

    if cat_var1 and cat_var2:
        # Cross-tabulation and percentage table
        st.subheader(f"a. Cross Tabulation of {cat_var1} and {cat_var2}")
        crosstab = pd.crosstab(df[cat_var1], df[cat_var2])
        st.write(crosstab)

        st.subheader(f"b. Proportion Table of {cat_var1} by {cat_var2}")
        prop_table = pd.crosstab(df[cat_var1], df[cat_var2], normalize='index') * 100
        st.write(prop_table.round(2))

        # Bar chart to visualize proportions
        st.subheader(f"c. Bar Chart of {cat_var1} by {cat_var2}")
        fig_bar = px.bar(prop_table, title=f"Proportion of {cat_var1} by {cat_var2}", labels={"value": "Percentage", "index": cat_var1},
                        color_discrete_sequence=px.colors.qualitative.Light24, barmode="group")
        st.plotly_chart(fig_bar)

        # Chi-square test for independence
        st.subheader(f"d. Chi-square Test of Independence Between {cat_var1} and {cat_var2}")
        chi2_result = stats.chi2_contingency(crosstab)
        st.write(f"Chi-square test result: χ² = {chi2_result[0]:.2f}, p-value = {chi2_result[1]:.3f}")

        # Generate dynamic finding based on Chi-square result
        st.write("**Finding:**")

        if chi2_result[1] < 0.05:
            st.write(f"- The p-value of the Chi-square test is {chi2_result[1]:.3f}, which is < 0.05.")
            st.write(f"- This suggests that {cat_var2} appears to have a significant effect on {cat_var1}.")
        else:
            st.write(f"- The p-value of the Chi-square test is {chi2_result[1]:.3f}, which is > 0.05.")
            st.write(f"- This suggests that {cat_var2} does not appear to have a significant effect on {cat_var1}.")

else:
    st.warning("No data loaded. Please go back to the Pre-EDA page to upload and process the data.")
