import streamlit as st
import pandas as pd
from agents.data_quality_agents import check_null_values, check_date_format, check_primary_key_duplicates, check_non_numerical_values, check_negative_numbers

# Streamlit App
st.title("Data Quality Check Tool")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Uploaded Data Preview")
    st.dataframe(df.head())
    
    # Buttons for individual checks
    if st.button("Check Null Values"):
        result = check_null_values(df)
        st.write("**Null Values:**", result)
    
    if st.button("Check Date Format"):
        result = check_date_format(df)
        st.write("**Date Format Issues:**", result)
    
    if st.button("Check Primary Key Duplicates"):
        result = check_primary_key_duplicates(df)
        st.write("**Primary Key Duplicates:**", result)
    
    if st.button("Check Non-Numerical Values"):
        result = check_non_numerical_values(df)
        st.write("**Non-Numerical Values:**", result)
    
    if st.button("Check Negative Numbers"):
        result = check_negative_numbers(df)
        st.write("**Negative Numbers:**", result)
