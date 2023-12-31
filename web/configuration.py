"""
A file for the configuration of the Sneek backend
"""
import json
import pathlib
from dataclasses import dataclass
from typing import Any, Dict

from typing_extensions import List

CONFIGURATION_FILENAME = pathlib.Path(__file__).parent.parent / "config.json"


@dataclass(frozen=True)
class Configuration:
    """
    A class that holds the data for the Sneek configuration
    """
    session_duration_in_hours: int
    channels: List[Dict[str, Any]]
    name_adjectives: List[str]
    name_animals: List[str]

    @classmethod
    def load(cls) -> "Configuration":
        """
        Loads the configuration from the configuration file
        """
        return cls(**json.loads(CONFIGURATION_FILENAME.read_text("utf-8")))
