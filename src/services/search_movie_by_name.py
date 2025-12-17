from typing import Any

from api import get_movies_data_by_api
from config import settings
from exceptions import SearchMovieNotFoundError
from logging_config import get_logger
from utils import MovieInfo, get_message_info_movie

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
                info_text=get_message_info_movie(movie),
            )
            for movie in movies_data
        ]
        logger.info("Successfully received data on films.")
        return movies_info
