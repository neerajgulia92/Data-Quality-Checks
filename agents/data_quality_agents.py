from langgraph.graph import StateGraph, START
from langchain_aws import ChatBedrock
from langchain_core.messages import SystemMessage, HumanMessage
from typing_extensions import TypedDict
import pandas as pd
import numpy as np

# Initialize the LLM
llm = ChatBedrock(
    credentials_profile_name="default", model_id="anthropic.claude-3-5-sonnet-20240620-v1:0"
)

# Define the Graph State
class DataQualityState(TypedDict):
    user_input: pd.DataFrame
    response: dict

def check_null_values(df: pd.DataFrame) -> dict:
    """Check for null values in the DataFrame."""
    return {"Null Values": df.isnull().sum().to_dict()}

def check_date_format(df: pd.DataFrame) -> dict:
    """Check if date columns have null values."""
    date_columns = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
    date_issues = {col: df[col].isnull().sum() for col in date_columns if df[col].isnull().sum() > 0}
    return {"Date Format Issues": date_issues}

def check_primary_key_duplicates(df: pd.DataFrame) -> dict:
    """Check for duplicate values in the first column (assumed to be the primary key)."""
    primary_key_column = df.columns[0]  # Assuming the first column is the PK
    duplicates = df.duplicated(subset=[primary_key_column]).sum()
    return {"Primary Key Duplicates": duplicates}

def check_non_numerical_values(df: pd.DataFrame) -> dict:
    """Check for non-numerical values in numerical columns."""
    numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    non_numerical_issues = {col: df[col].apply(lambda x: not isinstance(x, (int, float))).sum() for col in numerical_columns}
    return {"Non-Numerical Values": non_numerical_issues}

def check_negative_numbers(df: pd.DataFrame) -> dict:
    """Check for negative numbers in numerical columns."""
    numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    negative_numbers = {col: (df[col] < 0).sum() for col in numerical_columns}
    return {"Negative Numbers": negative_numbers}

# Create LangGraph workflows
workflow = StateGraph(DataQualityState)
workflow.add_sequence([check_null_values, check_date_format, check_primary_key_duplicates, check_non_numerical_values, check_negative_numbers])
workflow.add_edge(START, 'check_null_values')

# Compile the Graph
data_quality_graph = workflow.compile()