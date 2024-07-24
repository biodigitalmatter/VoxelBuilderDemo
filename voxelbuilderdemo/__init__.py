from pathlib import Path
from datetime import datetime
from numpy import asarray

REPO_DIR = Path(__file__).parent.parent
IMG_DIR = REPO_DIR / "data/img"

_timestamp = datetime.now()
TIMESTAMP = _timestamp.strftime("%y%m%d_%H%M%S")

NB_INDEX_DICT = {
    'up' : asarray([0,0,1]),
    'left' : asarray([-1,0,0]),
    'down' : asarray([0,0,-1]),
    'right' : asarray([1,0,0]),
    'front' : asarray([0,-1,0]),
    'back' : asarray([0,1,0])
}