from pathlib import Path

import cdsapi
import typer
from loguru import logger
from tqdm import tqdm

from compstat_research.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    # ----------------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    years = range(1940, 2025)

    logger.add("1.0-iragca-cds-data.log", rotation="500 MB", retention="7 days", compression="zip")
    logger.info(f"Starting download of ERA5 data from {years[0]} to {years[-1]}.")
    for year in tqdm(years, desc="Downloading data", unit="year"):
        try:
            dataset = "derived-era5-single-levels-daily-statistics"
            request = {
                "product_type": "reanalysis",
                "variable": ["2m_temperature"],
                "year": f"{year}",
                "month": [
                    "01", "02", "03",
                    "04", "05", "06",
                    "07", "08", "09",
                    "10", "11", "12"
                ],
                "day": [
                    "01", "02", "03",
                    "04", "05", "06",
                    "07", "08", "09",
                    "10", "11", "12",
                    "13", "14", "15",
                    "16", "17", "18",
                    "19", "20", "21",
                    "22", "23", "24",
                    "25", "26", "27",
                    "28", "29", "30",
                    "31"
                ],
                "daily_statistic": "daily_mean",
                "time_zone": "utc+08:00",
                "frequency": "1_hourly",
                "area": [20, 115, 5, 130]
            }

            client = cdsapi.Client()
            client.retrieve(dataset, request).download()
        except Exception as e:
            logger.error(f"Error downloading data for year {year}. Error: {e}")
            continue
        else:
            logger.info(f"Downloaded data for year {year}.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
