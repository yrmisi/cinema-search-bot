from aiogram import Bot
from aiogram.types import BotCommand

from logging_config import get_logger

logger = get_logger(__name__)


async def get_set_commands(bot: Bot) -> None:
    """ """
    logger.info("Setting up commands in the bot menu")

    commands_and_description = (
        ("start", "Запуск бота"),
        ("help", "Помощь"),
        ("search", "Поиск фильма или сериала по названию"),
        ("random", "Случайный выбор фильма или сериала"),
    )
    commands = [
        BotCommand(command=command, description=description) for command, description in commands_and_description
    ]
    await bot.set_my_commands(commands)
    logger.info("The commands were installed successfully.")
