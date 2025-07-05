# file: migrations/0001_create_gifts_table.sql
from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE IF NOT EXISTS gifts (
            gift_id        TEXT PRIMARY KEY,
            price          INTEGER NOT NULL DEFAULT 0,
            total_count    INTEGER,
            remaining_count INTEGER,
            is_limited     BOOLEAN NOT NULL DEFAULT FALSE,
            created_at     TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at     TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        """,
        "DROP TABLE gifts"
    )
]
