# PromptDB

PromptDB is a command-line interface (CLI) tool that allows users to query a MySQL database using natural language,
powered by OpenAI's ChatGPT. The tool converts natural language queries into SQL statements and executes them against a
MySQL database, making database interactions more intuitive and accessible.

## Features

- **Natural Language Processing**: Use natural language to write queries without needing to know SQL.
- **ChatGPT Integration**: Leverages OpenAI's ChatGPT to convert natural language into SQL queries.
- **Read-Only Mode**: Ensures data integrity by only executing read-only SQL queries (e.g., `SELECT` statements).
- **Schema Caching**: Caches the database schema to reduce overhead and speed up queries.
- **Configurable**: Easily configure database connection settings via a `config.json` file.

## Installation

To install PromptDB, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/promptdb.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd promptdb
    ```

3. **Install the package using pip**:

    ```bash
    pip install .
    ```

## Configuration

Before using PromptDB, you need to set up the configuration file (`config.json`) to connect to your MySQL database and
provide your OpenAI API key.

Create a `config.json` file in the root directory of the project with the following structure:

```json
{
    "mysql": {
        "host": "your_mysql_host",
        "user": "your_mysql_user",
        "password": "your_mysql_password",
        "database": "your_database_name"
    },
    "openai_api_key": "your_openai_api_key"
}
