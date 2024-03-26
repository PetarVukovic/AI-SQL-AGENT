from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from utilities.embeddings.hf_embeddings import SentenceTransformerEmbeddings
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

'''Docs
ChatOpenAI
Svrha: Služi za inicijalizaciju komunikacije sa OpenAI API-jem, konkretno sa modelom gpt-3.5-turbo. Omogućava slanje upita modelu i dobijanje odgovora.
Parametri:
model_name: Ime modela koji se koristi (u ovom slučaju gpt-3.5-turbo).
temperature: Kontroliše raznovrsnost odgovora. Nula znači da će model davati najverovatnije odgovore.
openai_api_key: Ključ za pristup OpenAI API-ju.

create_sql_agent
Svrha: Funkcija za kreiranje SQL agenta koji koristi jezički model za generisanje SQL upita na osnovu korisničkog unosa.
Parametri:
llm: Instanca jezičkog modela.
db: Baza podataka sa kojom agent interaguje.
verbose: Ako je postavljeno na True, štampa dodatne informacije tokom izvršavanja.

SemanticSimilarityExampleSelector
Svrha: Bira primere na osnovu semantičke sličnosti sa ulaznim upitom. Koristi se za selektovanje relevantnih primera koji pomažu modelu da generiše preciznije odgovore.
Metode:
from_examples: Inicijalizuje selektor sa setom primera, koristeći embeddinge za pronalaženje semantički sličnih primera.

OpenAIEmbeddings
Svrha: Generiše embeddinge (vektorske reprezentacije) koristeći OpenAI model. Ovi embeddingi se zatim koriste za pronalaženje semantički sličnih primera.

FAISS
Svrha: Biblioteka za efikasnu pretragu sličnosti i klasterizaciju gustih vektora. Koristi se u kombinaciji sa OpenAIEmbeddings za brzo pronalaženje sličnih primera.

ChatPromptTemplate, FewShotPromptTemplate, PromptTemplate, SystemMessagePromptTemplate
Ove klase se koriste za kreiranje promptova koji vode model kroz proces generisanja odgovora. Omogućavaju definisanje strukture prompta, dodavanje sistemskih poruka, i korišćenje few-shot learninga kroz primere input-output parova.
Kako Funkcioniše SQLAgent
Inicijalizacija ChatOpenAI: Postavlja osnovu za interakciju sa OpenAI jezičkim modelom.
Kreiranje SemanticSimilarityExampleSelector: Selektor koristi primere za identifikovanje onih koji su semantički najbliži upitu korisnika. Ovo poboljšava preciznost i relevantnost generisanih SQL upita.
Konstruisanje Promptova:
FewShotPromptTemplate: Uključuje nekoliko primera upita i odgovarajućih SQL upita kako bi pomogao modelu da razume kontekst zadataka.
ChatPromptTemplate: Kombinuje različite tipove promptova u jedan koherentan prompt, uključujući sistematske poruke i prostor za korisnički unos.
Kreiranje SQL Agenta: Konačno, funkcija create_sql_agent se koristi za kreiranje agenta koji koristi definisane promptove za generisanje SQL upita na osnovu korisničkog unosa. Ovaj agent je spreman za interakciju s korisnicima i pružanje odgovora na upite kroz generisane SQL upite.
Svaki od ovih koraka doprinosi stvaranju efikasnog sistema za interakciju s bazama podataka koristeći prirodni jezik, omogućavajući aplikacijama da procesuiraju korisničke upite i generišu odgovarajuće SQL upite na intuitivan način.
'''


class SQLAgent:
    def __init__(self,db):
        self.db = db

    def create_agent(self,examples):
   
        # SemanticSimilarityExampleSelector: Selects training examples based on semantic similarity to the input query.
        # from_examples: A method to initialize the selector with a set of examples.
        # OpenAIEmbeddings: Generates embeddings (vector representations) of examples using OpenAI's model.
        # FAISS: A library for efficient similarity search and clustering of dense vectors.
        # k: The number of similar examples to retrieve.
        # input_keys: Specifies which part of the examples to consider for generating embeddings.
        self.llm=ChatOpenAI()
        embeddings = SentenceTransformerEmbeddings()
        

        example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples,
            embeddings,
            vectorstore_cls= FAISS,
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
            verbose=False,
            agent_type="openai-tools",
        )

        return agent
