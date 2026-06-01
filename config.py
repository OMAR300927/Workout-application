from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    secret_key: SecretStr
    database_url: str

    imagekit_public_key: str
    imagekit_private_key: str
    imagekit_url: str

    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Setting() #type: ignore