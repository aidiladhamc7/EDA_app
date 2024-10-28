import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from module.EDA_BE import display_eda_info, round_decimal_columns, check_duplicates, remove_duplicates

# Insert Tittle and markdown
st.title("Exploratory Data Analysis🕵️")
st.markdown("### Univariate Analysis🎪")