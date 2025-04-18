# PROPERTIES
from enum import Enum

GAME_PROPERTIES_FILE = f"assets/save/game"


class Properties(Enum):
    LAST_SCORE = "last_score"
    MAX_SCORE = "max_score"
