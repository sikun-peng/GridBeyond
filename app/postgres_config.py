from pydantic_settings import BaseSettings, SettingsConfigDict

class PostgresConfig(BaseSettings):
    db_name: str = "gridbeyond"
    user: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: str = "5432"

    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env")