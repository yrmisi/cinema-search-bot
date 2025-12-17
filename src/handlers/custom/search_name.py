from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message, URLInputFile, User
from aiogram.utils.markdown import hbold

from exceptions import SearchMovieNotFoundError
from logging_config import get_logger
from services import SearchMovieNameService
from utils import MovieInfo, SearchMovieNameState

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

    movie_name: str | None = message.text

    if movie_name is None:
        return await message.answer("По этому запросу ничего не нашёл 😔")

    try:
        movies_info: list[MovieInfo] = SearchMovieNameService.get_movies(movie_name)
    except SearchMovieNotFoundError as exc:
        logger.error(exc.message)
        return await message.answer("По этому запросу ничего не нашёл 😔")

    for movie in movies_info:
        if movie.poster_url.startswith("http"):
            input_photo: URLInputFile | FSInputFile = URLInputFile(movie.poster_url)
        else:
            input_photo = FSInputFile(movie.poster_url)

        await message.answer_photo(photo=input_photo, caption=movie.info_text)

    return await message.answer(f"{hbold("Я могу еще поискать")} 📽")
