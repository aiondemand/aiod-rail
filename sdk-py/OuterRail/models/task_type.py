import json
from enum import Enum

from typing_extensions import Self

"""
    Enum describing type of tasks.
    allowed enum values: IMAGE_CLASSIFICATION, OBJECT_DETECTION, TEXT_CLASSIFICATION, TOKEN_CLASSIFICATION, 
        QUESTION_ANSWERING, TRANSLATION, SUMMARIZATION, TEXT_GENERATION, OTHER
"""


class TaskType(str, Enum):
    """
    allowed enum values
    """
    IMAGE_CLASSIFICATION = "IMAGE_CLASSIFICATION"
    OBJECT_DETECTION = "OBJECT_DETECTION"
    TEXT_CLASSIFICATION = "TEXT_CLASSIFICATION"
    TOKEN_CLASSIFICATION = "TOKEN_CLASSIFICATION"
    QUESTION_ANSWERING = "QUESTION_ANSWERING"
    TRANSLATION = "TRANSLATION"
    SUMMARIZATION = "SUMMARIZATION"
    TEXT_GENERATION = "TEXT_GENERATION"
    OTHER = "OTHER"

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of TaskType from a JSON string"""
        return cls(json.loads(json_str))
