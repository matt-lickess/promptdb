import json
import sys
from typing import TypedDict


class MySQLConfig(TypedDict):
    host: str
    user: str
    password: str
    database: str


class Config(TypedDict):
    mysql: MySQLConfig
    openai_api_key: str


def load_config() -> Config:
    """Load configuration from config.json file."""
    try:
        with open('config.json') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: config.json file not found. Please ensure the configuration file is in the correct location.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: config.json contains invalid JSON. Please check the file format.")
        sys.exit(1)
