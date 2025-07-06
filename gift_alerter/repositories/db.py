import aiopg
from aiopg.pool import Cursor
from contextlib import asynccontextmanager
from psycopg2.extras import RealDictCursor  # type: ignore
from typing import AsyncGenerator

from gift_alerter import settings
from gift_alerter.logger.logger import get_logger


logger = get_logger(__name__)

@asynccontextmanager
async def get_connection(dsn=settings.RESOURCES.POSTGRES.DSN) -> AsyncGenerator[Cursor, None]:
    async with aiopg.connect(dsn=str(dsn)) as conn:
        async with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Начинаем транзакцию вручную
            await cur.execute("BEGIN")
            try:
                yield cur  # выполняем пользовательские запросы
                await cur.execute("COMMIT")  # фиксация
            except Exception:
                await cur.execute("ROLLBACK")
                raise
