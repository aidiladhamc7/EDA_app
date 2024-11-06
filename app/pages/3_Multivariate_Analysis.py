import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the data from session state
if 'cleaned_data' in st.session_state:
    df = st.session_state['cleaned_data']
    
    st.title("Multivariate Analysis")

    # 1. Correlation Analysis
    st.header("1. Correlation Analysis")
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    correlation_matrix = df[numeric_columns].corr()
    fig_corr = px.imshow(correlation_matrix, text_auto=True, title="Correlation Matrix")
    st.plotly_chart(fig_corr)
    st.write("The correlation matrix shows relationships between numerical variables. Look for strong positive or negative correlations for deeper analysis.")

    # 2. Scatter Plot for Relationships
    st.header("2. Scatter Plot for Relationships")
    col1, col2 = st.columns(2)
    x_axis = col1.selectbox("Select the X-axis variable", numeric_columns, key="scatter_x")
    y_axis = col2.selectbox("Select the Y-axis variable", numeric_columns, key="scatter_y")
    
    if x_axis != y_axis:
        fig_scatter = px.scatter(df, x=x_axis, y=y_axis, title=f"Scatter Plot of {x_axis} vs. {y_axis}", trendline="ols")
        st.plotly_chart(fig_scatter)
        st.write("The scatter plot helps visualize the relationship between two numerical variables. A trendline indicates linear trends, if present.")

    # 3. Group Comparison
    st.header("3. Group Comparison")
    categorical_columns = df.select_dtypes(include=['object']).columns
    if len(categorical_columns) > 0:
        group_col = st.selectbox("Select a categorical column for group comparison", categorical_columns)
        compare_col = st.selectbox("Select a numeric column to compare across groups", numeric_columns)

        fig_box = px.box(df, x=group_col, y=compare_col, title=f"Box Plot of {compare_col} by {group_col}")
        st.plotly_chart(fig_box)
        st.write("The box plot compares the distribution of a numerical variable across different groups. Look for differences in median, range, and outliers.")

        # Conduct ANOVA or T-test based on the selected column
        st.write("**Statistical Test**: To confirm if differences between groups are statistically significant, an ANOVA or T-test could be applied.")

    # 4. Interaction Effects
    st.header("4. Interaction Effects")
    third_var = st.selectbox("Select a third variable for interaction effects", categorical_columns)
    
    if third_var != group_col:
        fig_interaction = px.scatter(df, x=x_axis, y=y_axis, color=third_var, title=f"Interaction of {x_axis} and {y_axis} by {third_var}")
        st.plotly_chart(fig_interaction)
        st.write(f"The interaction plot shows how the relationship between {x_axis} and {y_axis} varies based on {third_var}. Look for group-level differences in trends or clustering patterns.")

    # 5. Regression Analysis
    st.header("5. Regression Analysis")
    target_var = st.selectbox("Select a target variable for prediction", numeric_columns)
    predictor_vars = st.multiselect("Select predictor variables for regression analysis", numeric_columns.drop(target_var))
    
    if predictor_vars:
        X = df[predictor_vars].dropna()
        y = df[target_var].dropna()
        
        model = LinearRegression()
        model.fit(X, y)
        r_squared = model.score(X, y)
        st.write(f"**R-squared**: {r_squared:.2f}")
        st.write("An R-squared value close to 1 indicates a strong predictive relationship. Lower values suggest weaker predictive power.")

    # 6. Cluster Analysis (if clustering is relevant)
    st.header("6. Cluster Analysis")
    num_clusters = st.slider("Select the number of clusters", min_value=2, max_value=10, value=3)
    
    if len(numeric_columns) > 1:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df[numeric_columns].dropna())
        kmeans = KMeans(n_clusters=num_clusters, random_state=0)
        clusters = kmeans.fit_predict(scaled_data)
        df['Cluster'] = clusters

        fig_cluster = px.scatter(df, x=numeric_columns[0], y=numeric_columns[1], color='Cluster', title="Cluster Analysis")
        st.plotly_chart(fig_cluster)
        st.write(f"The cluster analysis groups data into {num_clusters} clusters. Look for natural groupings or segmentations that might inform decisions.")

else:
    st.warning("No data loaded. Please go back to the Pre-EDA page to upload and process the data.")
