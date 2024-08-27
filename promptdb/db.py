import logging
import sys
from typing import Dict, Any

import mysql.connector
from mysql.connector import MySQLConnection

from .cache import schema_cache

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def connect_to_db(config: Dict[str, Any]) -> MySQLConnection:
    """Connect to the MySQL database using provided configuration."""
    try:
        connection = mysql.connector.connect(
            host=config['mysql']['host'],
            user=config['mysql']['user'],
            password=config['mysql']['password'],
            database=config['mysql']['database']
        )
        logging.info("Successfully connected to the MySQL database.")
        return connection

    except mysql.connector.InterfaceError as err:
        logging.error(f"Interface error: Unable to connect to the MySQL database. {err}")
        sys.exit(1)
    except mysql.connector.DatabaseError as err:
        logging.error(f"Database error: Unable to connect to the MySQL database. {err}")
        sys.exit(1)
    except mysql.connector.Error as err:
        logging.error(f"Error: Unable to connect to the MySQL database. {err}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)


def get_db_schema(cursor) -> Dict[str, Any]:
    """Fetch the database schema and cache it."""
    if schema_cache:
        logging.info("Fetching schema from cache...")
        return schema_cache

    logging.info("Fetching schema from the database...")
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        schema = {}
        for (table_name,) in tables:
            cursor.execute(f"DESCRIBE `{table_name}`")  # Protect table names against SQL injection
            schema[table_name] = cursor.fetchall()

        # Cache the schema
        schema_cache.update(schema)
        logging.info("Schema fetched and cached successfully.")
        return schema

    except mysql.connector.Error as err:
        logging.error(f"Error: Unable to fetch schema from the database. {err}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)
