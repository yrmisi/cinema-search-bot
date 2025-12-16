from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class BotConfig(BaseSettings):
    """ """

    token: Annotated[str | None, Field(alias="BOT_TOKEN")] = None

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        extra="ignore",
    )


class PoiskkinoAPIConfig(BaseSettings):
    """ """

    key: Annotated[str | None, Field(alias="API_KEY")] = None
    url: str = "https://api.kinopoisk.dev/v1.4/movie/search"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        extra="ignore",
    )


class Settings(BaseModel):
    """ """

    bot_conf: BotConfig = BotConfig()
    poiskkino_api: PoiskkinoAPIConfig = PoiskkinoAPIConfig()

    @property
    def poiskkino_headers(self) -> dict[str, str]:
        """ """
        return {"accept": "application/json", "X-API-KEY": self.poiskkino_api.key or ""}


settings = Settings()
