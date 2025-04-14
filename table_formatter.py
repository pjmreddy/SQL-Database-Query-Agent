import pandas as pd
import streamlit as st
from typing import List, Tuple, Any

def format_query_results(results: List[Tuple], columns: List[str] = None):
    if not results:
        return "No results found."
    
    df = pd.DataFrame(results, columns=columns)
    return df

def format_as_markdown(results: List[Tuple], columns: List[str] = None):
    if not results:
        return "No results found."
    
    if not columns:
        columns = [f"Column {i+1}" for i in range(len(results[0]))]
    
    markdown = "| " + " | ".join(columns) + " |\n"
    markdown += "| " + " | ".join(["---" for _ in columns]) + " |\n"
    
    for row in results:
        markdown += "| " + " | ".join([str(item) for item in row]) + " |\n"
    
    return markdown