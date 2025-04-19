# PROPERTIES
from enum import Enum

from src.resource_manager import resource_path

GAME_PROPERTIES_FILE = resource_path("assets/save/game")


class Properties(Enum):
    LAST_SCORE = "last_score"
    MAX_SCORE = "max_score"
