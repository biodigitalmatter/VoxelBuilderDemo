from pathlib import Path
from datetime import datetime

REPO_DIR = Path(__file__).parent.parent
IMG_DIR = REPO_DIR / "data/img"

_timestamp = datetime.now()
TIMESTAMP = _timestamp.strftime("%y%m%d_%H%M%S")
