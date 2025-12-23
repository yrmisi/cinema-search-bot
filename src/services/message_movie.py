from database.models import Movie
from logging_config import get_logger
from utils import MovieInfo

logger = get_logger(__name__)


class MessageMovie:
    message_length_tg: int = 1024
    ellipsis: str = "..."

    @classmethod
    def get_message_info_movie(cls, movie: MovieInfo | Movie) -> str:
        """Generating a film information message."""
        logger.info("Message successfully created")
        return cls.set_message_length(
            f"{movie.description}\n\n"
            f"<code>Название:</code> {movie.name}\n"
            f"<code>Тип:</code> {movie.movie_or_series}\n"
            f"<code>Продолжительность:</code> {movie.duration}\n"
            f"<code>Бюджет:</code> {movie.budget}\n"
            f"<code>Рейтинг:</code> {movie.rating_imdb} IMDb\n"
            f"                      {movie.rating_kp} КиноПоиск\n"
            f"<code>Страны:</code> {movie.countries}\n"
            f"<code>Жанры:</code> {movie.genres}\n"
            f"<code>Премьера:</code> {movie.year} год\n"
        )

    @classmethod
    def set_message_length(cls, msg: str) -> str:
        """Checking the message length and truncating it if it is exceeded"""
        logger.info("Checking the message length")
        current_msg_len: int = len(msg)

        if current_msg_len <= cls.message_length_tg:
            logger.info("The message length does not exceed the set size")
            return msg

        msg_lines: list[str] = msg.split("\n")

        description: str = msg_lines[0]
        number_char_to_del: int = current_msg_len - cls.message_length_tg - len(cls.ellipsis)

        last_index: int = len(description) - number_char_to_del
        last_space_index: int = description[:last_index].rfind(" ")

        msg_lines[0] = description[:last_space_index] + cls.ellipsis

        logger.info("Successfully trimmed the message")
        return "\n".join(msg_lines)
