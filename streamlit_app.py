import streamlit as st
import pandas as pd
from data_quality_agents import data_quality_graph

# Streamlit App
st.title("Data Quality Check Tool")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Uploaded Data Preview")
    st.dataframe(df.head())
    
    # Run Data Quality Checks
    result = data_quality_graph.invoke({"user_input": df})
    
    # Display Results
    st.write("### Data Quality Report")
    for check, outcome in result["response"].items():
        st.write(f"**{check}:**", outcome)