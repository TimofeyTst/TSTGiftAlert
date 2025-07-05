from functools import lru_cache
import urllib.parse

from dotenv import find_dotenv
from pydantic import PostgresDsn, SecretStr, root_validator
from pydantic_settings import BaseSettings

class _Settings(BaseSettings):

    class Config:
        """Configuration of settings."""

        #: str: env file encoding.
        env_file_encoding = "utf-8"
        #: str: allow custom fields in model.
        arbitrary_types_allowed = True
        #: bool: case-sensitive for env variables.
        case_sensitive = True
        #: str: delimiter for nested env variables.
        env_nested_delimiter = "__"


class Resource(_Settings):
    """Resource base settings."""

    HOST: str
    PORT: int

    DSN: str | None

    def build_dsn(cls, values: dict):  # pylint: disable=no-self-argument
        raise NotImplementedError

class Postgresql(Resource):
    """Postgresql settings."""

    #: str: Postgresql host.
    HOST: str = "localhost"
    #: PositiveInt: positive int (x > 0) port of postgresql.
    PORT: int = 5432
    #: str: Postgresql user.
    USER: str = "postgres"
    #: SecretStr: Postgresql password.
    PASSWORD: SecretStr = SecretStr("postgres")
    #: str: Postgresql database name.
    DATABASE_NAME: str = "postgres"

    #: PositiveInt: Min count of connections in one pool to postgresql.
    MIN_CONNECTION: int = 1
    #: PositiveInt: Max count of connections in one pool  to postgresql.
    MAX_CONNECTION: int = 16

    #: str: Concatenation all settings for postgresql in one string. (DSN)
    DSN: PostgresDsn

    @root_validator(pre=True)
    def build_dsn(cls, values: dict):  # pylint: disable=no-self-argument
        values["DSN"] = PostgresDsn.build(
            scheme="postgresql",
            username=f"{values.get('USER')}",
            password=f"{urllib.parse.quote_plus(values.get('PASSWORD'))}",
            host=f"{values.get('HOST')}",
            port=int(values.get('PORT')),
            path=f"{values.get('DATABASE_NAME')}",
        )
        return values

class Resources(_Settings):
    POSTGRES: Postgresql

class Settings(_Settings):
    RESOURCES: Resources

    BOT_TOKEN: str
    CHANNEL_ID: str

    # Service behaviour
    ONLY_LIMITED: bool = True  # Alert only limited-amount gifts
    POLLING_TIMEOUT: int = 3   # Seconds between polling cycles

    LOGGER_FOLDER_PATH: str = "logs"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""

    return Settings(_env_file=find_dotenv(env_file))
