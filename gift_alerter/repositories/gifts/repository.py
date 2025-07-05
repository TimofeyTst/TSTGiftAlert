from aiopg.pool import Cursor
from typing import List, Set, AsyncGenerator

from gift_alerter.logger.logger import get_logger

logger = get_logger(__name__)


async def get_existing_gift_ids(cur: Cursor, gift_ids: List[str]) -> Set[str]:
    query = """
        SELECT gift_id
        FROM gifts
        WHERE gift_id = ANY(%(ids)s)
    """

    await cur.execute(query, {"ids": gift_ids})
    result = await cur.fetchall()
    logger.info(f"got existing gift ids: {len(result)}/{len(gift_ids)}")
    return {item['gift_id'] for item in result}

async def insert_gifts(cur: Cursor, gifts_data: List[dict]) -> None:
    rows_sql_parts = []
    for gift in gifts_data:
        rows_sql_parts.append(
            cur.mogrify("(%(gift_id)s,%(price)s,%(total_count)s,%(remaining_count)s,%(is_limited)s)", {
                "gift_id": gift.get("id"),
                "price": gift.get("price", 0),
                "total_count": gift.get("total_count"),
                "remaining_count": gift.get("remaining_count"),
                "is_limited": gift.get("total_count") is not None,
            }).decode()
        )

    if not rows_sql_parts:
        return

    values_clause = ", ".join(rows_sql_parts)
    query = f"""
        INSERT INTO gifts (gift_id, price, total_count, remaining_count, is_limited)
        VALUES {values_clause}
        ON CONFLICT (gift_id) DO NOTHING;
    """

    await cur.execute(query)
    logger.info("Inserted %d gifts", len(rows_sql_parts))
