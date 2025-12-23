import uuid


def create_search_id() -> str:
    """Generate random search ID."""
    return str(uuid.uuid4())[:6]
