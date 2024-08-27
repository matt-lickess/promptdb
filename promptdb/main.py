import mysql.connector

from .api import query_chatgpt
from .cache import clear_schema_cache
from .config import load_config
from .db import connect_to_db, get_db_schema
from .utils import format_schema_for_prompt, is_read_only_query, print_results


def main():
    # Load config
    config = load_config()

    # Connect to MySQL
    db_connection = connect_to_db(config)
    cursor = db_connection.cursor()

    while True:
        # User input
        user_input = input("Enter your query in natural language (or type 'exit' to quit): ")

        # Exit command
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the application. Goodbye!")
            break

        # Clear schema cache command
        if user_input.lower() == "clear cache":
            clear_schema_cache()
            continue

        # Get schema (from cache or database)
        schema = get_db_schema(cursor)
        formatted_schema = format_schema_for_prompt(schema)

        # Generate SQL query using ChatGPT
        prompt = f"Generate a read-only SQL query for the following database schema:\n{formatted_schema}\nUser query: {user_input}"
        gpt_response = query_chatgpt(config['openai_api_key'], prompt)

        # Extract SQL from ChatGPT response
        try:
            response_text = gpt_response['choices'][0]['message']['content'].strip()
        except (KeyError, IndexError):
            print("Error: Received unexpected response format from ChatGPT API.")
            continue

        print()
        print(f"Attempting Query:")
        print(response_text)

        # Check if the response is a read-only SQL query
        if is_read_only_query(response_text):
            # Execute SQL query
            try:
                cursor.execute(response_text)
                print_results(cursor)

            except mysql.connector.Error as err:
                print(f"Error: Failed to execute SQL query. {err}")
        else:
            # If the response is not a read-only SQL query, warn the user
            print("Warning: Generated query is not read-only. Query execution aborted to protect data integrity.")

    # Close connection
    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
