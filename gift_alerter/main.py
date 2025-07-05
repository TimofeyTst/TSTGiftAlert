from .services.alerter import service as alerter
from .logger.logger import get_logger

logger = get_logger(__name__)


def main() -> None:
    alerter.GiftAlerter().start()

if __name__ == "__main__":
    logger.info("settings...")
    main()
