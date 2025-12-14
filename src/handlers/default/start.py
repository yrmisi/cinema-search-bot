from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.formatting import Bold, Text

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> Message:
    """
    This handler receives messages with `/start` command
    """
    full_name: str = message.from_user.full_name if message.from_user else "user"
    entities: Text = Text("Hello ,", Bold(full_name), "!")

    return await message.answer(**entities.as_kwargs())
