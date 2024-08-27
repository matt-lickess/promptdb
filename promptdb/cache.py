schema_cache = {}


def clear_schema_cache() -> None:
    """Clears the schema cache."""
    global schema_cache
    schema_cache = {}
    print("Schema cache cleared.")
