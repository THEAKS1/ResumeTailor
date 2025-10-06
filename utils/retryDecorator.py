"""
retryDecorator.py

Provides a decorator to retry async functions on Google GenAI ServerError.
"""

import asyncio
from google.genai.errors import ServerError
from config import MAX_RETRY_PER_AGENT, DELAY_BETWEEN_RETRIES

def retry_on_server_error(func):
    """
    A decorator that retries an async function if a ServerError is encountered.
    """
    async def wrapper(*args, **kwargs):
        for attempt in range(MAX_RETRY_PER_AGENT):
            try:
                # Try running the function
                return await func(*args, **kwargs)
            except ServerError as e:
                print(f"Warning: '{func.__name__}' encountered a ServerError (Attempt {attempt + 1}/{MAX_RETRY_PER_AGENT}): {e}")
                if attempt < MAX_RETRY_PER_AGENT - 1:
                    print(f"Retrying in {DELAY_BETWEEN_RETRIES} seconds...")
                    await asyncio.sleep(DELAY_BETWEEN_RETRIES)
                else:
                    print(f"Error: Final attempt failed for '{func.__name__}'.")
                    raise
    return wrapper
