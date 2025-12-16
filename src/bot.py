import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from exceptions import TokenNotFoundError
from handlers.custom import search_router
from handlers.default import echo_router, start_router
from logging_config import get_logger
from utils import get_set_commands

logger = get_logger(__name__)


async def main() -> None:
    logger.info("Start polling.")
    # Dispatcher is a root router
    dp = Dispatcher()
    # Register all the routers from handlers package
    dp.include_routers(
        search_router,
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
    await get_set_commands(bot)

    me = await bot.get_me()
    logger.info(
        "Run polling for bot @%s id=%s - '%s'.",
        me.username,
        me.id,
        me.first_name or "cinema_search",
    )
    # And the run events dispatching
    await dp.start_polling(bot)
    logger.info(
        "Polling stopped for bot @%s id=%s - '%s'.",
        me.username,
        me.id,
        me.first_name or "cinema_search",
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
        logger.info("Polling stopped")
    except TokenNotFoundError as exc:
        logger.error(exc.message)
