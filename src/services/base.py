from typing import Any

from api_client import get_movie_by_id_api
from config import settings
from logging_config import get_logger
from utils import MovieInfo

logger = get_logger(__name__)


class BaseService:
    """Base class for the service"""

    is_budget: bool = True
    value_unknown: str = "неизвестно"

    @classmethod
    def get_movie_info(
        cls,
        movie: dict[str, Any],
        chat_id: int,
        search_id: str,
        page: int = 1,
    ) -> MovieInfo:
        movie_info: MovieInfo = MovieInfo(
            poster_url=(movie.get("poster") or {}).get("previewUrl") or settings.poiskkino_api.poster_not_found,
            description=movie.get("description") or "Описание отсутствует",
            name=movie.get("name") or cls.value_unknown,
            movie_or_series="фильм" if movie["type"] == "movie" else "сериал",
            duration=cls.get_duration_movie_or_series(movie),
            budget=cls.get_budget_value(movie),
            rating_imdb=movie["rating"]["imdb"],
            rating_kp=round(movie["rating"]["kp"], 1),
            countries=", ".join(country["name"] for country in movie["countries"]),
            genres=", ".join(genre["name"] for genre in movie["genres"]),
            year=movie["year"],
            chat_id=chat_id,
            search_id=search_id,
            page=page,
        )
        return movie_info

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
