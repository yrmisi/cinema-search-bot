from typing import Any

from api_client import get_movies_by_data_api
from database.models import Movie
from database.repository import create_movie_db
from exceptions import PoiskkinoAPIError, SearchMovieNotFoundError
from logging_config import get_logger
from utils import MovieInfo, MovieSearchResult

from .base import BaseService

logger = get_logger(__name__)


class SearchMovieNameService(BaseService):
    """ """

    is_budget: bool = False

    @classmethod
    async def get_movies(cls, movie_name: str, chat_id: int, search_id: str) -> MovieSearchResult:
        """ """
        logger.info("Film data processing.")
        query_data: dict[str, str] = {"query": movie_name}
        try:
            movies_data: list[dict[str, Any]] = get_movies_by_data_api(query_data)
        except PoiskkinoAPIError as exc:
            logger.warning(exc.message)
            raise

        if not movies_data:
            logger.error("No data found for the film.")
            raise SearchMovieNotFoundError()

        movies: list[MovieInfo] = [
            cls.get_movie_info(movie, chat_id, search_id, page) for page, movie in enumerate(movies_data, start=1)
        ]
        movie: Movie = await create_movie_db(movies)
        total_pages: int = len(movies_data)

        logger.info("Successfully received data on films.")
        return MovieSearchResult(movie=movie, total_pages=total_pages)
