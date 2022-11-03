def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == 'hello':
        return 'hi'
    
    return 'Didn\'t understand'