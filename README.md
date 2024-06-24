# LLM_SQLTalk

## Overview
LLM_SQLTalk is a Streamlit application designed to interact with a SQL database using a language model agent. Users can select a query input, which the agent then translates into a SQL query to fetch relevant results from the database.

## Features
- User-friendly interface for selecting queries.
- Utilizes advanced language model capabilities to generate SQL queries.
- Connects to a SQL database and retrieves relevant data.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/PetarVukovic/LLM_SQLTalk.git
    cd LLM_SQLTalk
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables (ensure you have an OpenAI API key):
    ```bash
    export OPENAI_API_KEY='your_openai_api_key'  # On Windows: set OPENAI_API_KEY=your_openai_api_key
    ```

5. Run the application:
    ```bash
    streamlit run app.py
    ```

## Usage
1. Select an input from the dropdown menu.
2. The application will generate and execute the corresponding SQL query.
3. View the results displayed on the Streamlit interface.

## Project Structure
- `app.py`: Main application script.
- `sql_agent.py`: Defines the `SQLAgent` class for interacting with the SQL database.
- `selecting_query.py`: Utility function to match user input with the corresponding SQL query.
- `examples.py`: Contains example inputs and their corresponding SQL queries.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License.
