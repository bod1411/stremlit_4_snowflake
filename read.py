import os
import configparser
import pandas as pd
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session

# Snowflake connection function
@st.cache_resource(show_spinner="Connecting to Snowflake...")
def get_session():
    try:
        return get_active_session()
    except:
        parser = configparser.ConfigParser()
        parser.read(os.path.join(os.path.expanduser('~'), ".snowsql/config"))
        section = "connections.demo_conn"
        pars = {
            "account": parser.get(section, "accountname"),
            "user": parser.get(section, "username"),
            "password": os.environ['SNOWSQL_PWD']
        }
        return Session.builder.configs(pars).create()

# Function to execute Snowflake query and return DataFrame
@st.cache_data(show_spinner="Running a Snowflake query...")
def get_dataframe(query):
    try:
        conn = get_session()
        st.write(f"Executing query: {query}")
        result = conn.sql(query)
        rows = result.collect()
        st.write(f"Number of rows retrieved: {len(rows)}")
        if len(rows) == 0:
            st.warning("The query returned no results. The table might be empty.")
        return pd.DataFrame(rows).convert_dtypes()
    except Exception as e:
        st.error(f"Error executing query: {str(e)}")
        return None

# Main Streamlit app
def main():
    st.title("Employee Data Viewer")

    st.header("EMP Table Data")
    query = "SELECT * FROM DEV.PRASAD.EMP"
    df = get_dataframe(query)
    if df is not None and not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No data available in the table.")
    
    # Add a count query
    count_query = "SELECT COUNT(*) as row_count FROM DEV.PRASAD.EMP"
    count_df = get_dataframe(count_query)
    if count_df is not None and not count_df.empty:
        st.write(f"Total number of rows in the table: {count_df.iloc[0]['ROW_COUNT']}")

if __name__ == "__main__":
    main()

