from aiogram.types import FSInputFile, URLInputFile

from logging_config import get_logger

logger = get_logger(__name__)


def build_poster_input(poster_url: str) -> URLInputFile | FSInputFile:
    """Converts a string (URL or local path) into an appropriate aiogram InputFile."""
    logger.info("Converts string")

    if poster_url.startswith("http"):
        logger.info("Convert string from url")
        return URLInputFile(poster_url)

    logger.info("Convert string local path")
    return FSInputFile(poster_url)
