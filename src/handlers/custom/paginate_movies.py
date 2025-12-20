from typing import Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InaccessibleMessage, InputMediaPhoto

from keyboards.inlines import build_movie_kb
from utils import MovieInfo, build_poster_input

router = Router()


@router.callback_query(F.data.in_({"movie_prev", "movie_next"}))
async def paginate_movies_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    movies_raw: list[dict[str, Any]] = data.get("movies", [])
    index: int = data.get("index", 0)

    if not movies_raw:
        await callback.answer("Список фильмов пуст")
        return

    total = len(movies_raw)

    if callback.data == "movie_prev" and index > 0:
        index -= 1
    elif callback.data == "movie_next" and index < total - 1:
        index += 1
    else:
        await callback.answer()
        return

    await state.update_data({"index": index})

    movie = MovieInfo(**movies_raw[index])
    input_photo = build_poster_input(movie.poster_url)
    kb = build_movie_kb(index, total)

    msg = callback.message

    # защита от None и InaccessibleMessage
    if msg is None or isinstance(msg, InaccessibleMessage):
        await callback.answer("Сообщение недоступно")
        return

    await msg.edit_media(
        media=InputMediaPhoto(media=input_photo, caption=movie.info_text),
        reply_markup=kb,
    )

    await callback.answer()
