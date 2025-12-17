from typing import Any

from aiogram.utils.markdown import hcode

from logging_config import get_logger

from .message_length import set_message_length

logger = get_logger(__name__)


def get_message_info_movie(movie: dict[str, Any]) -> str:
    """Generating a film information message."""
    logger.info("Message successfully created")
    return set_message_length(
        f"{movie.get("description") or "Описание отсутствует"}\n\n"
        f"{hcode("Название:")} {movie["name"]}\n"
        f"{hcode("Тип:")} {"фильм" if movie["type"] == "movie" else "сериал"}\n"
        f"{hcode("Продолжительность:")} {
                        str(movie.get("movieLength")) + " мин."
                        if movie.get("movieLength")
                        else str(movie.get("seriesLength")) + " серий"
                        }\n"
        f"{hcode("Рейтинг:")} {movie["rating"]["imdb"]} IMDb\n"
        f"                      {round(movie["rating"]["kp"], 1)} КиноПоиск\n"
        f"{hcode("Страны:")} {", ".join(country["name"] for country in  movie["countries"])}\n"
        f"{hcode("Жанры:")} {", ".join(genre["name"] for genre in  movie["genres"])}\n"
        f"{hcode("Премьера:")} {movie["year"]} год\n"
    )
