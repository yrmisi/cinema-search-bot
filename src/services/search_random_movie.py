from typing import Any

from api import random_movie_by_api
from config import settings
from exceptions import LimitIterateAPIError
from logging_config import get_logger
from utils import MovieInfo, get_message_info_movie

logger = get_logger(__name__)


class RandomMovieService:
    """ """

    @staticmethod
    def get_random_movies() -> MovieInfo:
        """ """
        logger.info("Film data processing.")

        try:
            movie: dict[str, Any] = random_movie_by_api()
        except LimitIterateAPIError as exc:
            logger.warning(exc.message)
            raise

        movie_info: MovieInfo = MovieInfo(
            poster_url=(movie.get("poster") or {}).get("previewUrl") or settings.poiskkino_api.poster_not_found,
            info_text=get_message_info_movie(movie),
        )
        return movie_info
