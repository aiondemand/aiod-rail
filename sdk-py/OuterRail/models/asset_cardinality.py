import json

from enum import Enum
from typing_extensions import Self


"""
    Enumerator for asset cardinality.
    allowed enum values: 0-N, 1-N, 1-1
"""


class AssetCardinality(str, Enum):
    ENUM_0_MINUS_N = "0-N"
    ENUM_1_MINUS_N = "1-N"
    ENUM_1_MINUS_1 = "1-1"

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of AssetCardinality from a JSON string"""
        return cls(json.loads(json_str))
