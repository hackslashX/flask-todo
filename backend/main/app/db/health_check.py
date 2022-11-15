""" Database Health Check """

import logging

from app.db.session import SessionLocal
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(300),
    wait=wait_fixed(1),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def health_check() -> None:
    """Check if database is up and running."""
    logger.info("Checking database connection...")
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
    except Exception as e:
        logger.error(e)
        logging.error("Failed to connect to database")
        raise e
    else:
        logging.info("Database connection successful")


if __name__ == "__main__":
    health_check()
