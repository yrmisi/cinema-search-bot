from typing import Any

import requests
from requests.exceptions import HTTPError

from config import settings
from exceptions import PoiskkinoAPIError
from logging_config import get_logger

logger = get_logger(__name__)


def get_movies_by_data_api(add_search_params: dict[str, str]) -> list[dict[str, Any]]:
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
    except HTTPError as exc:
        raise PoiskkinoAPIError(f"HTTP error {exc.response.status_code} from poiskkino API")

    logger.info("API data received successfully")
    return response.json().get("docs")


def get_movie_by_id_api(movie_id: int) -> dict[str, Any]:
    """Get a movie or TV series by ID."""
    logger.debug(
        "API URL with a random movie ID: %s",
        settings.poiskkino_api.url_by_id.format(movie_id),
    )
    response = requests.get(
        url=settings.poiskkino_api.url_by_id.format(movie_id),
        headers=settings.poiskkino_headers,
    )
    logger.info("data received successfully from the API")
    return response.json()
