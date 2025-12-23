import uuid


def create_search_id() -> str:
    """ """
    return str(uuid.uuid4())[:6]
