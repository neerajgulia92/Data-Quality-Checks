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

def check_null_values(state: DataQualityState) -> DataQualityState:
    df = state["user_input"]
    return {"response": {"Null Values": df.isnull().sum().to_dict()}}

def check_date_format(state: DataQualityState) -> DataQualityState:
    df = state["user_input"]
    date_columns = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
    date_issues = {col: df[col].isnull().sum() for col in date_columns if df[col].isnull().sum() > 0}
    return {"response": {"Date Format Issues": date_issues}}

def check_primary_key_duplicates(state: DataQualityState) -> DataQualityState:
    df = state["user_input"]
    primary_key_column = df.columns[0]  # Assuming first column is PK
    duplicates = df.duplicated(subset=[primary_key_column]).sum()
    return {"response": {"Primary Key Duplicates": duplicates}}

def check_non_numerical_values(state: DataQualityState) -> DataQualityState:
    df = state["user_input"]
    numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    non_numerical_issues = {col: df[col].apply(lambda x: not isinstance(x, (int, float))).sum() for col in numerical_columns}
    return {"response": {"Non-Numerical Values": non_numerical_issues}}

def check_negative_numbers(state: DataQualityState) -> DataQualityState:
    df = state["user_input"]
    numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    negative_numbers = {col: (df[col] < 0).sum() for col in numerical_columns}
    return {"response": {"Negative Numbers": negative_numbers}}

# Create LangGraph workflows
workflow = StateGraph(DataQualityState)
workflow.add_sequence([check_null_values, check_date_format, check_primary_key_duplicates, check_non_numerical_values, check_negative_numbers])
workflow.add_edge(START, 'check_null_values')

# Compile the Graph
data_quality_graph = workflow.compile()