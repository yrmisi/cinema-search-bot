import json

from aiogram import F, Router
from aiogram.types import CallbackQuery, InaccessibleMessage, InputMediaPhoto

from database import get_movie_db
from keyboards.inlines import build_movie_kb
from services import MessageMovieService
from utils import build_poster_input

router = Router()


@router.callback_query(F.data.startswith("{"))
async def paginate_movies_callback(callback: CallbackQuery):
    """ """

    data = callback.data

    if not data:
        await callback.answer("Список фильмов пуст")
        return

    data_dict: dict[str, str | int] = json.loads(data)

    chat_id = int(data_dict["c_id"])
    search_id = str(data_dict["s_id"])
    page = int(data_dict["page"])

    movie = await get_movie_db(chat_id, search_id, page)

    if not movie:
        await callback.answer("Список фильмов пуст")
        return

    input_photo = build_poster_input(movie.poster_url)
    message_movie = MessageMovieService.get_message_info_movie(movie)
    kb = build_movie_kb(chat_id, search_id, page)

    msg = callback.message

    # защита от None и InaccessibleMessage
    if msg is None or isinstance(msg, InaccessibleMessage):
        await callback.answer("Сообщение недоступно")
        return

    await msg.edit_media(
        media=InputMediaPhoto(
            media=input_photo,
            caption=message_movie,
        ),
        reply_markup=kb,
    )
    await callback.answer(text="Страница обновлена!", show_alert=False)
