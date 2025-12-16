from typing import Any

import requests

from config import settings
from exceptions import PoiskkinoAPIError
from logging_config import get_logger

logger = get_logger(__name__)


def get_movies_data_by_api(add_search_params: dict[str, str]) -> list[dict[str, Any]]:
    logger.info("We receive data via API")

    params = {"page": 1, "limit": 10} | add_search_params
    logger.debug("Data params: %s", params)

    try:
        response = requests.get(
            url=settings.poiskkino_api.url,
            headers=settings.poiskkino_headers,
            params=params,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        raise PoiskkinoAPIError(f"HTTP error {exc.response.status_code} from poiskkino API")

    logger.info("API data received successfully")
    return response.json().get("docs")
