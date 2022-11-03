def get_response(message: str) -> str | None:
    p_message = message.lower()

    if p_message == 'hello':
        return 'hi'