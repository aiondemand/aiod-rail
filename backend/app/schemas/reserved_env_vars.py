from enum import Enum


class ReservedEnvVars(str, Enum):
    MODEL_NAMES = "MODEL_NAMES"
    DATASET_NAMES = "DATASET_NAMES"
    MODEL_IDS = "MODEL_IDS"
    DATASET_IDS = "DATASET_IDS"
