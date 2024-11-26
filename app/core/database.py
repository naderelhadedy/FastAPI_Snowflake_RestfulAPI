"""
Database module
"""
import snowflake.connector as snowflake_connector
from contextlib import contextmanager
from app.core.config import Config


@contextmanager
def setup_snowflake_connection():
    """
    setup snowflake connection
    """
    snowflake_config = Config.load_snowflake_connection_configs()

    sf_connection = snowflake_connector.connect(
        **snowflake_config
    )

    try:
        yield sf_connection
    finally:
        sf_connection.close()
