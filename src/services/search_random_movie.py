from typing import Any

from api_client import get_movie_by_id_api
from database.models import Movie
from database.repository import create_movie_db
from exceptions import LimitIterateAPIError
from logging_config import get_logger
from utils import MovieInfo, get_secret_randint

from .base import BaseService

logger = get_logger(__name__)


class RandomMovieService(BaseService):
    """ """

    @classmethod
    async def get_random_movies(
        cls,
        chat_id: int,
        search_id: str,
    ) -> Movie:
        """ """
        logger.info("Film data processing.")

        try:
            movie_random: dict[str, Any] = cls.random_movie()
        except LimitIterateAPIError as exc:
            logger.warning(exc.message)
            raise

        movie_info: MovieInfo = cls.get_movie_info(movie_random, chat_id, search_id)
        movie: Movie = await create_movie_db(movie_info)
        return movie

    @staticmethod
    def random_movie() -> dict[str, Any]:
        """We select a random movie by ID"""
        logger.info("We select a random movie API")

        for _ in range(5):
            random_movie_id: int = get_secret_randint()
            logger.debug("Random movie ID: %s", random_movie_id)
            movie_data: dict[str, Any] = get_movie_by_id_api(random_movie_id)
            logger.debug("Movie data: %s", movie_data)

            if len(movie_data) > 3:
                logger.info("Successful receipt of a random movie")
                return movie_data

        raise LimitIterateAPIError()
