import secrets


def generate_state() -> str:
    """
    Generate a secure random state value for OAuth.
    """
    return secrets.token_urlsafe(32)