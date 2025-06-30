import json

from enum import Enum
from typing_extensions import Self

"""
    Enumerator for states of experiment runs.
    allowed enum values: CREATED, IN_PROGRESS, FINISHED, CRASHED
"""


class RunState(str, Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    CRASHED = "CRASHED"

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of RunState from a JSON string"""
        return cls(json.loads(json_str))
