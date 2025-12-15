import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from exceptions import TokenNotFoundError
from handlers.default import echo_router, start_router


async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # Register all the routers from handlers package
    dp.include_routers(
        start_router,
        echo_router,
    )
    token: str | None = settings.bot_conf.token

    if token is None:
        raise TokenNotFoundError()

    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except TokenNotFoundError as exc:
        logging.error(exc.message)
