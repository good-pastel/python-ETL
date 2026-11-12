from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT_NAME = "Python ETL Pipeline"
INPUT_FOLDER = ROOT / "demo" / "input"
OUTPUT_FOLDER = ROOT / "demo" / "output"
OUTPUT_FILE = OUTPUT_FOLDER / "Result.xlsx"

SUPPORTED_FILES = (".csv", ".xlsx", ".xls", ".zip")
DATE_COLUMN = "Timestamp"
DATE_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
    "%m/%d/%Y %H:%M",
    "%m/%d/%Y %H:%M:%S",
    "%m/%d/%Y %I:%M %p",
    "%m/%d/%Y %I:%M:%S %p",
    "%b %d, %Y %H:%M",
    "%b %d, %Y %H:%M:%S",
    "%B %d, %Y %H:%M",
    "%B %d, %Y %H:%M:%S",
]

DAY_FIRST = True
START_DATE = "2025-03-01 00:00:00"
END_DATE = "2025-03-31 23:59:59"

SPLIT_SHEET_BY_MONTH = True
SHEET_NAME = "Data"
MAX_ROWS_PER_SHEET = 1_048_576
AUTO_SPLIT_SHEET = True
FREEZE_HEADER = True
AUTO_FILTER = True
AUTO_COLUMN_WIDTH = True
FORMULA_PROTECTION = True
REMOVE_ILLEGAL_CHARACTERS = True
CREATE_SUMMARY_SHEET = True
SHOW_LOG = True
