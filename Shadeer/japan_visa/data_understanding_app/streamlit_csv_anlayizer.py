import streamlit as st
import pandas as pd

def analyze_csv(file):
    # Read the CSV file
    df = pd.read_csv(file)
    
    # Get the first few rows (head)
    head = df.head()
    
    # Data format of every column
    data_format = pd.DataFrame(df.dtypes, columns=['Data Type'])
    
    # Calculate missing values
    missing_values = df.isnull().sum().to_frame('Missing Values')
    missing_percentage = (df.isnull().sum() / len(df) * 100).to_frame('Percentage Missing')
    missing_info = pd.concat([missing_values, missing_percentage], axis=1)
    
    # Duplicate understanding
    duplicate_count = df.duplicated().sum()
    duplicate_columns = df.apply(lambda x: x.duplicated().sum()).to_frame('Duplicate Count')
    
    # Compute basic statistics
    basic_stats = df.describe()
    
    return head, data_format, missing_info, duplicate_count, duplicate_columns, basic_stats

# Streamlit app
st.title("CSV File Analyzer")
st.write("Upload a CSV file to view its head, data format, missing values, duplicates, and basic statistics.")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    head, data_format, missing_info, duplicate_count, duplicate_columns, basic_stats = analyze_csv(uploaded_file)
    
    st.subheader("First Few Rows")
    st.dataframe(head)
    
    st.subheader("Data Format of Each Column")
    st.dataframe(data_format)
    
    st.subheader("Missing Values")
    st.dataframe(missing_info)
    
    st.subheader("Duplicates")
    st.write(f"Total duplicate rows: {duplicate_count}")
    st.dataframe(duplicate_columns)
    
    st.subheader("Basic Statistics")
    st.dataframe(basic_stats)
