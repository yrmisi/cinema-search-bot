from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, User
from aiogram.utils.formatting import Bold, Text

from logging_config import get_logger

logger = get_logger(__name__)
router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> Message:
    """
    This handler receives messages with `/start` command
    """
    user: User | None = message.from_user
    if user:
        logger.info(
            "The user (full name - %s, id - %s) pressed the command 'start'.",
            user.full_name,
            user.id,
        )
    full_name: str = message.from_user.full_name if message.from_user else "user"
    entities: Text = Text("Hello ,", Bold(full_name), "!")

    return await message.answer(**entities.as_kwargs())
