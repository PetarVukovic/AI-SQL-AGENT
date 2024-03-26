import streamlit as st
import os
from agents.sql_agent import SQLAgent
from langchain_community.utilities import SQLDatabase
from examples import examples
from sqlalchemy import create_engine
from utilities.connection_string import get_connection_string
from utilities.selecting_query import get_query

def main():
    st.title("Chat with SQL Agent 📂💭📔")
    st.subheader("Below, select your SQL Server and Database and input your query")

    ex=examples.get_examples()
    # Select server
    server = st.selectbox("Select server: ", ['', "localhost\\SQLEXPRESS", "baja"], index=0)
    if not server:
        st.warning("Please select a server")
        st.stop()

    #Select database
    database = st.selectbox("Select database: ", ['', "Reactivities", "AdnetBalancingMarket_Local"], index=0)
    if not database:
        st.warning("Please select a database")
        st.stop()
        
    

    # Attempt to establish a database connection
    conn_str = get_connection_string(server, database)
    try:
        db_engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}")
        db = SQLDatabase(db_engine)
        st.success("Connection successful!")
    except Exception as e:
        st.error(f"Connection failed: {e}")
        st.stop()
        
    #Select input you wont match with query
    input_querys = [d["input"] for d in ex]
    input_query = st.selectbox("Select information you wont retrieve: ", input_querys, index=0)
    if not input_query:
        st.warning("Please select SQL query you wont execute")
        st.stop()
        
    
    #Get query matched with input
    matched_query = get_query(ex, input_query)  
    api_token = os.getenv("OPENAI_API_KEY")
    st.write("API Token:", api_token)  # Ovo
    if api_token:
        sql_agent = SQLAgent(db)
        agent = sql_agent.create_agent(ex)  # Assuming create_agent is correctly defined
        result = agent.invoke({"input": matched_query})
        st.write(result['output'])
    else:
        st.error("OpenAI API key is not provided")

if __name__ == "__main__":
    main()
