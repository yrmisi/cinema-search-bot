"""Module for creating and configuring a logger."""

import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler

from config import BASE_DIR

# Используем UTC для всех логов
logging.Formatter.converter = time.gmtime

os.makedirs(BASE_DIR / "logs", exist_ok=True)


def get_logger(name: str = "bot") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:  # избегаем дублирования обработчиков
        logger.setLevel(logging.DEBUG)

        file_handler = TimedRotatingFileHandler(
            BASE_DIR / "logs/bot.log",
            when="midnight",
            interval=1,
            backupCount=30,
            encoding="utf-8",
        )
        file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.propagate = False

    return logger
