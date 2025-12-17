from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message, URLInputFile, User

from exceptions import LimitIterateAPIError
from logging_config import get_logger
from services import RandomMovieService
from utils import MovieInfo, build_poster_input

logger = get_logger(__name__)
router = Router()


@router.message(Command("random"))
async def random_movie_handler(message: Message):
    """The handler generates and sends a random movie or TV series."""
    user: User | None = message.from_user
    if user:
        logger.info(
            "The user (full name - %s, id - %s) sent a random message",
            user.full_name,
            user.id,
        )
    try:
        movie_info: MovieInfo = RandomMovieService.get_random_movies()
        input_photo: URLInputFile | FSInputFile = build_poster_input(movie_info.poster_url)

        return await message.answer_photo(photo=input_photo, caption=movie_info.info_text)
    except LimitIterateAPIError as exc:
        logger.warning(exc.message)
        return await message.answer("🎬 К сожалению, сейчас не удалось найти фильм. Попробуйте снова через пару минут!")
