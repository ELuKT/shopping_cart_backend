import secrets

# https://stackoverflow.com/questions/817882/unique-session-id-in-python
def generate_request_id():
    """
    Creates a cryptographically-secure, URL-safe string
    """
    return secrets.token_urlsafe(16) 