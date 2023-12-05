from enum import Enum


class TemplateState(str, Enum):
    CREATED = "CREATED"
    BUILDING_IMAGE = "BUILDING_IMAGE"
    PUSHING_IMAGE = "PUSHING_IMAGE"
    FINISHED = "FINISHED"
    CRASHED = "CRASHED"


class RunState(str, Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    CRASHED = "CRASHED"
    FINISHED = "FINISHED"
