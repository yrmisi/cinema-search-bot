from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User
from aiogram.utils.markdown import hbold

from exceptions import PoiskkinoAPIError, SearchMovieNotFoundError
from keyboards.inlines import build_movie_kb
from logging_config import get_logger
from services import MessageMovieService, SearchMovieNameService
from utils import MovieSearchResult, SearchMovieNameState, build_poster_input, create_search_id

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
    search_id: str = create_search_id()
    try:
        movie_result: MovieSearchResult = await SearchMovieNameService.get_movies(
            movie_name,
            message.chat.id,
            search_id,
        )
    except SearchMovieNotFoundError as exc:
        logger.error(exc.message)
        return await message.answer("По этому запросу ничего не нашёл 😔")
    except PoiskkinoAPIError as exc:
        logger.warning(exc.message)
        return await message.answer("🎬 К сожалению, сейчас не удалось найти фильм. Попробуйте снова через пару минут!")

    input_photo = build_poster_input(movie_result.movie.poster_url)
    message_movie: str = MessageMovieService.get_message_info_movie(movie_result.movie)
    kb = build_movie_kb(message.chat.id, search_id, 1, movie_result.total_pages)

    await message.answer_photo(photo=input_photo, caption=message_movie, reply_markup=kb)
    return await message.answer(f"{hbold("Я могу еще поискать")} 📽")
