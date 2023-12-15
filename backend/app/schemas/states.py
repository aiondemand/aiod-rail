from enum import Enum


class TemplateState(str, Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    CRASHED = "CRASHED"


class RunState(str, Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    CRASHED = "CRASHED"
    FINISHED = "FINISHED"
