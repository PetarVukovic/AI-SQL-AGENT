# import os
# from langchain_community.tools.tavily_search import TavilySearchResults     
# tk=os.getenv('TAVILY_API_KEY')

# search = TavilySearchResults()
# print(search.invoke('What is wheater in Zagreb?'))
import pyodbc

# Define your connection parameters
server = 'localhost\\SQLEXPRESS'
database = 'Reactivities'
trusted_connection = 'yes'

# Construct the connection string
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};'

# Establish the connection
try:
    conn = pyodbc.connect(conn_str)
    print("Connection successful!")
    print("Connection URI:", conn_str)
except Exception as e:
    print(f"Connection failed: {e}")
