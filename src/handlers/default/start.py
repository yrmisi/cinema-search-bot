from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, User
from aiogram.utils.markdown import hbold, hitalic

from logging_config import get_logger

logger = get_logger(__name__)
router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> Message:
    """
    This handler receives messages with `/start` command
    """
    user: User | None = message.from_user
    if user:
        logger.info(
            "The user (full name - %s, id - %s) pressed the command 'start'.",
            user.full_name,
            user.id,
        )
    full_name: str = user.full_name if user else "пользователь"
    welcome_text = (
        f"🎬 Привет {hbold(full_name)}! Я помогу тебе найти любой фильм или сериал.\n\n"
        "Просто напиши название — и я покажу результаты с Кинопоиска.\n\n"
        f"💡 {hbold("Советы:")}\n"
        "• Можно искать по части названия: «Интерстелл»\n"
        "• Используй команды: /search, /help\n\n"
        f"{hitalic("Приятного просмотра!")} 🍿"
    )
    return await message.answer(welcome_text)
