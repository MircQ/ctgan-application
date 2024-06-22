from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuration(BaseSettings):

    PORT: int = Field(
        title="port",
        description="Port on which the microservice is running"
    )


CONFIG = Configuration(_env_file='.env', _env_file_encoding='utf-8')
