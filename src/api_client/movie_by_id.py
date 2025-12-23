from typing import Any

import requests

from config import settings
from logging_config import get_logger

logger = get_logger(__name__)


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
