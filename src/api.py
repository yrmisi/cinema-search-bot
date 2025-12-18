from typing import Any

import requests

from config import settings
from exceptions import LimitIterateAPIError, PoiskkinoAPIError
from logging_config import get_logger
from utils import get_secret_randint

logger = get_logger(__name__)


def get_movies_data_by_api(add_search_params: dict[str, str]) -> list[dict[str, Any]]:
    """ """
    logger.info("We receive data via API")

    params: dict[str, int | str] = {"page": 1, "limit": 10} | add_search_params
    logger.debug("Data params: %s", params)

    try:
        response = requests.get(
            url=settings.poiskkino_api.url_search,
            headers=settings.poiskkino_headers,
            params=params,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        raise PoiskkinoAPIError(f"HTTP error {exc.response.status_code} from poiskkino API")

    logger.info("API data received successfully")
    return response.json().get("docs")


def get_movie_by_id_api(movie_id: int) -> dict[str, Any]:
    """Get a movie or TV series by ID."""
    response = requests.get(
        url=settings.poiskkino_api.url_by_id.format(movie_id),
        headers=settings.poiskkino_headers,
    )
    logger.info("data received successfully from the API")
    return response.json()


def random_movie_by_api() -> dict[str, Any]:
    """We select a random movie by ID"""
    logger.info("We select a random movie API")

    for _ in range(5):
        random_movie_id: int = get_secret_randint()
        logger.debug(
            "API URL with a random movie ID: %s",
            settings.poiskkino_api.url_by_id.format(random_movie_id),
        )
        movie_data: dict[str, Any] = get_movie_by_id_api(random_movie_id)
        logger.debug("Movie data: %s", movie_data)

        if len(movie_data) > 3:
            logger.info("Successful receipt of a random movie")
            return movie_data

    raise LimitIterateAPIError()
