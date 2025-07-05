import asyncio
import aiohttp
from aiogram import Bot

from gift_alerter import settings
from gift_alerter.repositories.telegram import repository as tg_repo
from gift_alerter.services.gifts import service as gifts_service
from gift_alerter.logger.logger import get_logger
from gift_alerter.repositories.db import get_connection

logger = get_logger(__name__)


class GiftAlerter:
    """Service that fetches available Telegram gifts and sends an alert message to a channel."""

    UNLIMITED_SIGN = '∞'
    DEFAULT_EMOJI = '🎁'
    DEFAULT_STAR_COUNT = '??'

    def __init__(self) -> None:
        if not settings.BOT_TOKEN or not settings.CHANNEL_ID:
            raise ValueError("BOT_TOKEN and CHANNEL_ID must be provided in environment variables (.env file)")

        self.bot: Bot = Bot(token=settings.BOT_TOKEN)

    def _get_gift_info(self, gift: dict) -> str | None:
        emoji = gift.get("sticker", {}).get("emoji", self.DEFAULT_EMOJI)
        star_count = gift.get("star_count", self.DEFAULT_STAR_COUNT)
        total = gift.get("total_count", self.UNLIMITED_SIGN)

        if total == "Unlimited" and settings.ONLY_LIMITED:
            return None

        remaining = gift.get("remaining_count", self.UNLIMITED_SIGN)
        return f"{emoji} {star_count} ⭐️ - {remaining}/{total}"

    async def _build_message(self, gifts) -> str:
        lines: list[str] = []
        for gift in gifts:
            info = self._get_gift_info(gift)
            if info:
                lines.append(info)

        return "\n".join(lines)

    async def _send_alert(self, gifts) -> None:
        message_text = await self._build_message(gifts)
        await self.bot.send_message(chat_id=settings.CHANNEL_ID, text=message_text)

    async def process_new_gifts(self, gifts) -> None:
        logger.info("Alerting about new gifts in db transaction...")

        async with get_connection() as conn:
            await gifts_service.insert_new_gifts(conn, new_gifts)
            await self._send_alert(new_gifts)

    async def main_cycle(self) -> None:
        async with aiohttp.ClientSession() as session:
            try:
                while True:
                    logger.info("Fetching gifts...")

                    gifts = await tg_repo.get_available_gifts(bot_token=settings.BOT_TOKEN, session=session)
                    if not gifts:
                        logger.warning("Gift list is empty or with error, try to sleep 10s")
                        await asyncio.sleep(10)

                    logger.info("Filtering gifts...")
                    new_gifts = await gifts_service.filter_already_alerted(gifts)
                    if new_gifts:
                        logger.info(f"Find {len(new_gifts)} new_gifts: {new_gifts}")
                        await self.process_new_gifts(new_gifts)
                    else:
                        logger.info("No new gifts available at this moment")

                    logger.info(f"Sleeping {settings.POLLING_TIMEOUT} seconds...")
                    await asyncio.sleep(settings.POLLING_TIMEOUT)
            except KeyboardInterrupt:
                logger.error("Keyboard interrupt, stopping...")
                await self.bot.session.close()

    async def run_with_retry(self) -> None:
        while True:
            try:
                logger.info("Starting main cycle")
                await self.main_cycle()
            except Exception as e:
                logger.exception(f"PANIC: {e}, try to recovery after sleep 10s")
                await asyncio.sleep(10)
                continue

    def start(self) -> None:
        asyncio.run(self.run_with_retry()) 