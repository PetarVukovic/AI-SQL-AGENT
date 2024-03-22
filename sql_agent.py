
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

class SQLAgent:
    def __init__(self, api_key, db):
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)
        self.db = db

    def create_agent(self,examples):
        agent=create_sql_agent(llm=self.llm,db=self.db,verbose=True)
        
   
        # SemanticSimilarityExampleSelector: Selects training examples based on semantic similarity to the input query.
        # from_examples: A method to initialize the selector with a set of examples.
        # OpenAIEmbeddings: Generates embeddings (vector representations) of examples using OpenAI's model.
        # FAISS: A library for efficient similarity search and clustering of dense vectors.
        # k: The number of similar examples to retrieve.
        # input_keys: Specifies which part of the examples to consider for generating embeddings.

        example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples,
            OpenAIEmbeddings(),
            FAISS,
            k=5,
            input_keys=["input"],
        )

        system_prefix = """You are an agent designed to interact with a SQL database.
        Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for the relevant columns given the question.
        You have access to tools for interacting with the database.
        Only use the given tools. Only use the information returned by the tools to construct your final answer.
        You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

        If the question does not seem related to the database, just return "I don't know" as the answer.

        Here are some examples of user inputs and their corresponding SQL queries:"""
        
        
        
        # ChatPromptTemplate: Combines multiple prompt templates into a single, cohesive prompt for the agent.
        # FewShotPromptTemplate: Utilizes few-shot learning by providing examples of input-output pairs to help guide the agent.
        # PromptTemplate: A basic template for formatting examples.
        # SystemMessagePromptTemplate: Adds system-level instructions or information to the prompt.

        few_shot_prompt = FewShotPromptTemplate(
            example_selector=example_selector,
            example_prompt=PromptTemplate.from_template(
                "User input: {input}\nSQL query: {query}"
            ),
            input_variables=["input", "dialect", "top_k"],
            prefix=system_prefix,
            suffix="",
        )

        full_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate(prompt=few_shot_prompt),
                ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )

        agent = create_sql_agent(
            llm=self.llm,
            db=self.db,
            prompt=full_prompt,
            verbose=True,
            agent_type="openai-tools",
        )

        return agent
