import json

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def build_movie_kb(
    chat_id: int,
    search_id: str,
    page: int = 1,
    total: int = 10,
) -> InlineKeyboardMarkup:
    """ """
    buttons: list[InlineKeyboardButton] = []
    if page > 1:
        buttons.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=json.dumps(
                    {
                        "a": "p",
                        "c": chat_id,
                        "s": search_id,
                        "pg": page - 1,
                    }
                ),
            )
        )
    if page < total:
        buttons.append(
            InlineKeyboardButton(
                text="Вперёд ➡️",
                callback_data=json.dumps(
                    {
                        "a": "n",
                        "c": chat_id,
                        "s": search_id,
                        "pg": page + 1,
                    }
                ),
            )
        )
    button_info = [
        InlineKeyboardButton(
            text=f"{page} из {total} 🎥",
            callback_data="movie_info",
        )
    ]
    return (
        InlineKeyboardMarkup(inline_keyboard=[buttons, button_info])
        if buttons
        else InlineKeyboardMarkup(inline_keyboard=[button_info])
    )
