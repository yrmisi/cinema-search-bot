class BotBaseError(Exception):
    """Basic bot error."""

    pass


class TokenNotFoundError(BotBaseError):
    """Bot token not found."""

    def __init__(self, message: str = "BOT_TOKEN is not set in environment") -> None:
        self.message = message
        super().__init__(self.message)


class PoiskkinoAPIError(BotBaseError):

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class SearchMovieNotFoundError(BotBaseError):

    def __init__(self, message: str = "No data found while searching for the movie") -> None:
        self.message = message
        super().__init__(self.message)
