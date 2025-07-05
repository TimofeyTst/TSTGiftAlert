import aiohttp

from typing import List, Dict, Any

from gift_alerter.logger.logger import get_logger

logger = get_logger(__name__)


async def get_available_gifts(bot_token: str, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
    """Retrieve available gifts via Telegram Bot API.

    This is a minimal wrapper around the /getAvailableGifts endpoint used by the GiftAlerter service.
    Returns an empty list when no gifts are available or an error occurs.
    """
    url = f"https://api.telegram.org/bot{bot_token}/getAvailableGifts"
    try:
        async with session.get(url) as response:
            data = await response.json()
            if not data.get("ok"):
                logger.error(f"API response error: {data}, return empty list")

            return data.get("result", {}).get("gifts", [])
    except Exception as e:
        logger.error(f"Error while requesting /getAvailableGifts: {e}")
        return []
