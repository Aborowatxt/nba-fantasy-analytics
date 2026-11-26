import logging
from pathlib import Path

from src.extract import extract_player_logs
from src.transform import transform_player_logs
from src.load import load_player_logs

# Create directory for pipeline logs
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():

    logger.info("Starting NBA Fantasy Analytics Pipeline")

    try:
        # Extract
        raw_df = extract_player_logs()
        logger.info(f"Extracted {len(raw_df):,} records")

        # Transform
        cleaned_df = transform_player_logs(raw_df)
        logger.info(f"Validated {len(cleaned_df):,} records")
        logger.info(
            f"Removed {len(raw_df) - len(cleaned_df):,} records"
        )

        if cleaned_df.empty:
            raise ValueError("No valid records available for loading")

        # Load
        load_player_logs(cleaned_df)

        logger.info("ETL pipeline completed successfully")

    except Exception:
        logger.exception("ETL pipeline failed")
        raise


if __name__ == "__main__":
    main()