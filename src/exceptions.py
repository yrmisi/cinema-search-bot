class BotBaseError(Exception):
    """ """

    pass


class TokenNotFoundError(BotBaseError):
    """ """

    def __init__(self, message: str = "BOT_TOKEN is not set in environment") -> None:
        self.message = message
        super().__init__(self.message)
