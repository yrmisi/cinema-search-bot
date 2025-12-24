import secrets

from logging_config import get_logger

logger = get_logger(__name__)


def get_secret_randint(start_num: int = 250, stop_num: int = 15000000) -> int:
    """Secure random number generation."""
    logger.info("Random number generation")
    return start_num + secrets.randbelow(stop_num - start_num + 1)
