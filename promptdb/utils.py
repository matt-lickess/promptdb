import re
from typing import Dict, List, Tuple


def format_schema_for_prompt(schema: Dict[str, List[Tuple[str, str]]]) -> str:
    """Format the schema information for the ChatGPT prompt.

    Args:
        schema (Dict[str, List[Tuple[str, str]]]): A dictionary representing the database schema.
                                                   Keys are table names, and values are lists of tuples,
                                                   where each tuple contains a column name and type.

    Returns:
        str: A formatted string describing the schema for use in a ChatGPT prompt.
    """
    formatted_schema = []
    for table, columns in schema.items():
        column_descriptions = ', '.join(f"{col[0]} ({col[1]})" for col in columns)
        formatted_schema.append(f"Table: {table}, Columns: {column_descriptions}")
    return "\n".join(formatted_schema)


def is_read_only_query(response: str) -> bool:
    """
    Check if the response is a read-only SQL query.

    Args:
        response (str): The SQL query to check.

    Returns:
        bool: True if the query is read-only (SELECT), False otherwise.
    """
    # Remove comments from the query
    response = re.sub(r'(--[^\n]*)|(/\*[\s\S]*?\*/)', '', response, flags=re.MULTILINE).strip()

    # Convert query to uppercase for uniform comparison
    response_upper = response.upper()

    # Regular expression to match the beginning of a SELECT query
    read_only_pattern = re.compile(r"^\s*SELECT\s", re.IGNORECASE)

    # List of forbidden SQL commands (beginning words)
    forbidden_commands = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE', 'RENAME', 'TRUNCATE', 'REPLACE']

    # Check if the query starts with a read-only keyword
    if read_only_pattern.match(response):
        # Now we need to ensure no forbidden commands are the start of any SQL statements
        for command in forbidden_commands:
            forbidden_pattern = re.compile(rf"^\s*{command}\s", re.IGNORECASE)
            if forbidden_pattern.match(response_upper):
                return False
        return True
    else:
        return False


from typing import Any
import textwrap
from tabulate import tabulate


def print_results(cursor: Any, max_lines: int = 100, max_columns: int = 8, total_max_width: int = 160) -> None:
    """
    Print SQL query results with wrapped text, truncated rows, and limited columns.

    Args:
        cursor (Any): MySQL cursor object with executed query results.
        max_lines (int): Maximum number of lines (rows) to display.
        max_columns (int): Maximum number of columns to display.
        total_max_width (int): Maximum total width for text wrapping across all cells in a row.

    Returns:
        None
    """
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    # Determine if we need to truncate columns
    if len(columns) > max_columns:
        # Calculate the number of hidden columns
        hidden_columns_count = len(columns) - max_columns

        # Truncate columns and add a placeholder for the remaining columns
        columns = columns[:max_columns] + [f"... ({hidden_columns_count} columns hidden)"]
        # Convert each row to a list and truncate it to max_columns, then add ellipsis
        results = [list(row[:max_columns]) + ['...'] for row in results]

    # Limit rows to max_lines
    if len(results) > max_lines:
        print()
        print(f"Note: Displaying only the first {max_lines} rows out of {len(results)} available.")
        results = results[:max_lines]

    # Calculate max width per column dynamically based on total_max_width
    displayed_columns_count = min(len(columns), max_columns)
    if displayed_columns_count > 0:
        dynamic_max_width = total_max_width // displayed_columns_count
    else:
        dynamic_max_width = total_max_width

    # Wrap text in each cell to a maximum width
    wrapped_results = [
        [textwrap.fill(str(cell), width=dynamic_max_width) for cell in row]
        for row in results
    ]

    # Print formatted results using tabulate
    print()
    print(tabulate(wrapped_results, headers=columns))
    print()
