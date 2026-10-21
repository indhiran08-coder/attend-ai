from pathlib import Path

# Project root: /home/jetson/Desktop/Indiran
PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_DIR = PROJECT_DIR / "data" / "input"
OUTPUT_DIR = PROJECT_DIR / "data" / "output"
RESULTS_DIR = PROJECT_DIR / "results"
DATABASE_DIR = PROJECT_DIR / "database"

PERSON_CLASS_ID = 1
DETECTION_THRESHOLD = 0.50

TRACKER_IOU_THRESHOLD = 0.30
MAX_MISSED_FRAMES = 15

for directory in (
    INPUT_DIR,
    OUTPUT_DIR,
    RESULTS_DIR,
    DATABASE_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)
