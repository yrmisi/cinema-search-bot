import requests
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User

from config import settings
from logging_config import get_logger
from services import SearchMovieNameService
from utils import SearchMovieNameState

logger = get_logger(__name__)
router = Router()


@router.message(Command("search"))
async def search_by_name_handler(message: Message, state: FSMContext) -> Message:
    user: User | None = message.from_user
    if user:
        logger.info(
            "The user (full name - %s, id - %s) searches for a movie by title.",
            user.full_name,
            user.id,
        )
    await state.set_state(SearchMovieNameState.name)

    return await message.answer("Введите название фильма")


@router.message(SearchMovieNameState.name)
async def get_movie_by_name_handler(message: Message, state: FSMContext) -> Message:
    user: User | None = message.from_user
    if user:
        logger.info(
            "The user (full name - %s, id - %s) entered the title of the film.",
            user.full_name,
            user.id,
        )
    await state.clear()

    movie_name = message.text or ""

    movies_data = SearchMovieNameService.get_movies(movie_name)
    return await message.answer(movies_data)
