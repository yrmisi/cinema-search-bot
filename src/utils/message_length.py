from logging_config import get_logger

logger = get_logger(__name__)


def set_message_length(
    msg: str,
    message_length: int = 1024,
    ellipsis: str = "...",
) -> str:
    """Checking the message length and truncating it if it is exceeded"""
    logger.info("Checking the message length")
    current_msg_len: int = len(msg)

    if current_msg_len <= 1024:
        logger.info("The message length does not exceed the set size")
        return msg

    msg_lines: list[str] = msg.split("\n")

    description: str = msg_lines[0]
    number_char_to_del: int = current_msg_len - message_length - len(ellipsis)

    last_index: int = len(description) - number_char_to_del
    last_space_index: int = description[:last_index].rfind(" ")

    msg_lines[0] = description[:last_space_index] + ellipsis

    logger.info("Successfully trimmed the message")
    return "\n".join(msg_lines)
