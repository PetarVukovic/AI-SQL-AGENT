import streamlit as st
import os
from selecting_query import get_query
from sql_agent import SQLAgent
from langchain_community.utilities import SQLDatabase
from examples import examples


def main():
    st.title("App for Talking with SQL Agents 📔🕶")

    # Input for OpenAI API key
    api_key = st.text_input("Enter your OpenAI API key:", type="password")

    if not api_key:
        st.warning("Please enter your OpenAI API key.")
        st.stop()

    inputs = [d["input"] for d in examples]
    inp = st.selectbox("Input: ", inputs, index=None)

    if inp is None:
        st.stop()

    # Get matched query
    matched_query = get_query(examples, inp)

    # Initialize SQL agent
    db = SQLDatabase.from_uri("sqlite:///Chinook.db")
    sql_agent = SQLAgent(api_key, db)

    # Create agent using create_agent method
    agent = sql_agent.create_agent(examples)
    result = agent.invoke({"input": matched_query})

    st.write(result["output"])


if __name__ == "__main__":
    main()
