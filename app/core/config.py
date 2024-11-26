"""
Config module
"""
import tomli
from pathlib import Path


class Config:
    """
    Config class
    """
    config_path = "app/.snowflake/connections.toml"
    snowflake_config_name = "snowflake_connection"

    @classmethod
    def load_snowflake_connection_configs(cls):
        """
        load_snowflake_connection_configs
        """
        config_path = Path(cls.config_path)
        with open(config_path, "rb") as f:
            config = tomli.load(f)

        return config[cls.snowflake_config_name]
