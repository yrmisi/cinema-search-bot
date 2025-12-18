from typing import Any

from api import get_movie_by_id_api
from logging_config import get_logger

logger = get_logger(__name__)


class BaseService:
    """Base class for the service"""

    is_budget: bool = True
    value_unknown: str = "неизвестно"
    message_length_tg: int = 1024
    ellipsis: str = "..."

    @classmethod
    def get_message_info_movie(cls, movie: dict[str, Any]) -> str:
        """Generating a film information message."""
        description: str = movie.get("description") or "Описание отсутствует"
        movie_name: str = movie.get("name") or cls.value_unknown
        movie_or_series: str = "фильм" if movie["type"] == "movie" else "сериал"
        duration: str = cls.get_duration_movie_or_series(movie)
        budget: str = cls.get_budget_value(movie)
        rating_imdb: float = movie["rating"]["imdb"]
        rating_kp: float = round(movie["rating"]["kp"], 1)
        countries: str = ", ".join(country["name"] for country in movie["countries"])
        genres: str = ", ".join(genre["name"] for genre in movie["genres"])
        year: str = movie["year"]

        logger.info("Message successfully created")
        return cls.set_message_length(
            f"{description}\n\n"
            f"<code>Название:</code> {movie_name}\n"
            f"<code>Тип:</code> {movie_or_series}\n"
            f"<code>Продолжительность:</code> {duration}\n"
            f"<code>Бюджет:</code> {budget}\n"
            f"<code>Рейтинг:</code> {rating_imdb} IMDb\n"
            f"                      {rating_kp} КиноПоиск\n"
            f"<code>Страны:</code> {countries}\n"
            f"<code>Жанры:</code> {genres}\n"
            f"<code>Премьера:</code> {year} год\n"
        )

    @classmethod
    def get_duration_movie_or_series(cls, movie: dict[str, Any]) -> str:
        """Set the duration of a movie or TV series."""
        if movie.get("movieLength"):
            logger.info("I set the duration of the film")
            hours: int = movie["movieLength"] // 60
            min: int = movie["movieLength"] % 60
            return f"{hours:02}:{min:02}"

        elif movie.get("seriesLength"):
            logger.info("I set the duration of the TV series")
            return f"{movie.get("seriesLength")} серий"

        logger.info("The duration could not be set")
        return cls.value_unknown

    @classmethod
    def get_budget_value(cls, movie: dict[str, Any]) -> str:
        """Get the film's budget"""
        if not cls.is_budget:
            logger.info("There is no budget field in the data, we get it")
            movie = get_movie_by_id_api(movie["id"])

        value: int | None = (movie.get("budget") or {}).get("value")
        if value is None:
            logger.info("There is no budget value")
            return cls.value_unknown

        currency: str = movie["budget"]["currency"]

        logger.info("The budget value was successfully obtained")
        return f"{value}{currency}"

    @classmethod
    def set_message_length(cls, msg: str) -> str:
        """Checking the message length and truncating it if it is exceeded"""
        logger.info("Checking the message length")
        current_msg_len: int = len(msg)

        if current_msg_len <= cls.message_length_tg:
            logger.info("The message length does not exceed the set size")
            return msg

        msg_lines: list[str] = msg.split("\n")

        description: str = msg_lines[0]
        number_char_to_del: int = current_msg_len - cls.message_length_tg - len(cls.ellipsis)

        last_index: int = len(description) - number_char_to_del
        last_space_index: int = description[:last_index].rfind(" ")

        msg_lines[0] = description[:last_space_index] + cls.ellipsis

        logger.info("Successfully trimmed the message")
        return "\n".join(msg_lines)
