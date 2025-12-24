from aiogram import Router
from aiogram.types import Message, User

from logging_config import get_logger

logger = get_logger(__name__)
router = Router()


@router.message()
async def echo_handler(message: Message) -> Message:
    """
    Handler will forward receive a message back to the sender.
    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    user: User | None = message.from_user
    if user:
        logger.info(
            "The user (full name - %s, id - %s) wrote an unspecified message with the command.",
            user.full_name,
            user.id,
        )
    try:
        # Send a copy of the received message
        return await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        return await message.answer("Nice try!")
