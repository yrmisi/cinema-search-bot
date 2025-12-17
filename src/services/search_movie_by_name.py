from typing import Any

from aiogram.utils.markdown import hcode

from api import get_movies_data_by_api
from config import settings
from exceptions import SearchMovieNotFoundError
from logging_config import get_logger
from utils import MovieInfo, set_message_length

logger = get_logger(__name__)


class SearchMovieNameService:
    """ """

    @staticmethod
    def get_movies(movie_name: str) -> list[MovieInfo]:
        """ """
        logger.info("Film data processing.")
        query_data: dict[str, str] = {"query": movie_name}
        movies_data: list[dict[str, Any]] = get_movies_data_by_api(query_data)

        if not movies_data:
            logger.error("No data found for the film.")
            raise SearchMovieNotFoundError()

        movies_info: list[MovieInfo] = [
            MovieInfo(
                poster_url=(movie.get("poster") or {}).get("previewUrl") or settings.poiskkino_api.poster_not_found,
                info_text=set_message_length(
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
                ),
            )
            for movie in movies_data
        ]
        logger.info("Successfully received data on films.")
        return movies_info
