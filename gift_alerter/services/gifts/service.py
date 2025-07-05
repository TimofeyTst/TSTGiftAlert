from typing import List, Dict, Any

from gift_alerter.repositories.db import get_connection
from gift_alerter.repositories.gifts import repository as gifts_repo


async def filter_already_alerted(gifts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    gift_ids = [gift['id'] for gift in gifts]

    async with get_connection() as conn:
        new_gift_ids = await gifts_repo.get_existing_gift_ids(conn, gift_ids)

    result = []
    for gift in gifts:
        if gift['id'] in new_gift_ids:
            continue
        result.append(gift)

    return result


async def insert_new_gifts(session, gifts: List[Dict[str, Any]]) -> None:
    await gifts_repo.insert_gifts(session, gifts)
