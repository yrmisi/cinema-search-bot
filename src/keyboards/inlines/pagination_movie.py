from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def build_movie_kb(index: int, total: int) -> InlineKeyboardMarkup:
    buttons: list[InlineKeyboardButton] = []
    if index > 0:
        buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data="movie_prev"))
    if index < total - 1:
        buttons.append(InlineKeyboardButton(text="Вперёд ➡️", callback_data="movie_next"))

    button_info = [
        InlineKeyboardButton(
            text=f"{index + 1} из {total} 🎥",
            callback_data="movie_info",
        )
    ]
    return (
        InlineKeyboardMarkup(inline_keyboard=[buttons, button_info])
        if buttons
        else InlineKeyboardMarkup(inline_keyboard=[])
    )
