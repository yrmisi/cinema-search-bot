from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, User
from aiogram.utils.markdown import hbold

from logging_config import get_logger

logger = get_logger(__name__)
router = Router()


@router.message(Command("help"))
async def help_handler(message: Message) -> Message:
    """Sends help on bot commands"""
    user: User | None = message.from_user
    if user:
        logger.info(
            "The user (full name - %s, id - %s) requested help.",
            user.full_name,
            user.id,
        )
    help_text: str = (
        f"👋 {hbold("Привет! Я бот для поиска фильмов и сериалов.")}\n\n"
        "Вот что я умею:\n"
        "🎬 /search — найти фильм или сериал\n"
        "⭐ /favorites — показать ваше избранное\n"
        "🔔 /notify — включить уведомления о новых сериях\n"
        "⚙️ /settings — настройки поиска и уведомлений\n\n"
        "💡 Совет: просто напишите мне — я попробую найти случайный фильм или сериал!\n\n"
        "Если возникли вопросы — напишите разработчику: @cinema_search_robot_bot"
    )
    return await message.answer(help_text)
