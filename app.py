# import streamlit as st          
# import os 
# from langchain_openai import ChatOpenAI
# from langchain_community.agent_toolkits import create_sql_agent
# from langchain_community.utilities import SQLDatabase
# import streamlit as st
# from examples import examples
# from langchain_community.vectorstores import FAISS
# from langchain_core.example_selectors import SemanticSimilarityExampleSelector
# from langchain_openai import OpenAIEmbeddings
# from langchain_core.prompts import (
#     ChatPromptTemplate,
#     FewShotPromptTemplate,
#     MessagesPlaceholder,
#     PromptTemplate,
#     SystemMessagePromptTemplate,
# )
# from selectingQuery import get_query


# st.title("App for talking with SQL agents 📔🕶")
             


# #Utils

# api_key=os.getenv('OPENAI_API_KEY')
# db=SQLDatabase.from_uri('sqlite:///Chinook.db')

# values = []
# keys=[]
# # Uncomprehensive for loop to extract values
# inputs = [d["input"] for d in examples]


# inp=st.selectbox("Input: ", inputs, index=None)

# if inp is None:
#     st.stop()

# matched_query = get_query(examples,inp)

# llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)

# agent=create_sql_agent(llm=llm,db=db,verbose=True)


# #Custom prompt
# examples = examples


# example_selector = SemanticSimilarityExampleSelector.from_examples(
#     examples,
#     OpenAIEmbeddings(),
#     FAISS,
#     k=5,
#     input_keys=["input"],
# )

# system_prefix = """You are an agent designed to interact with a SQL database.
# Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
# Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
# You can order the results by a relevant column to return the most interesting examples in the database.
# Never query for all the columns from a specific table, only ask for the relevant columns given the question.
# You have access to tools for interacting with the database.
# Only use the given tools. Only use the information returned by the tools to construct your final answer.
# You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

# DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

# If the question does not seem related to the database, just return "I don't know" as the answer.

# Here are some examples of user inputs and their corresponding SQL queries:"""

# few_shot_prompt = FewShotPromptTemplate(
#     example_selector=example_selector,
#     example_prompt=PromptTemplate.from_template(
#         "User input: {input}\nSQL query: {query}"
#     ),
#     input_variables=["input", "dialect", "top_k"],
#     prefix=system_prefix,
#     suffix="",
# )

# full_prompt = ChatPromptTemplate.from_messages(
#     [
#         SystemMessagePromptTemplate(prompt=few_shot_prompt),
#         ("human", "{input}"),
#         MessagesPlaceholder("agent_scratchpad"),
#     ]
# )

# # Example formatted prompt
# prompt_val = full_prompt.invoke(
#     {
#         "input": "How many arists are there",
#         "top_k": 5,
#         "dialect": "SQLite",
#         "agent_scratchpad": [],
#     }
# )


# agent = create_sql_agent(
#     llm=llm,
#     db=db,
#     prompt=full_prompt,
#     verbose=True,
#     agent_type="openai-tools",
# )

# result=agent.invoke({"input": matched_query})
# st.write(result['output'])

import streamlit as st
import os
from selecting_query import get_query
from sql_agent import SQLAgent
from langchain_community.utilities import SQLDatabase
from examples import examples

def main():
    st.title("App for talking with SQL agents 📔🕶")
    inputs = [d["input"] for d in examples]
    inp = st.selectbox("Input: ", inputs, index=None)
    if inp is None:
        st.stop()
    
    # Get matched query
    matched_query = get_query(examples, inp)
    
    # Initialize SQL agent
    api_key = os.getenv('OPENAI_API_KEY')
    db = SQLDatabase.from_uri('sqlite:///Chinook.db')
    sql_agent = SQLAgent(api_key, db)
    
    # Create agent using create_agent method
    agent = sql_agent.create_agent(examples)
    result=agent.invoke({"input": matched_query})
    st.write(result['output'])

if __name__ == "__main__":
    main()
