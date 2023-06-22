# TODO: All this code needs to be replaced by proper functionality when possible
from pydantic import BaseModel


class Model(BaseModel):
    platform: str
    platform_identifier: str
    description: str
    name: str
    same_as: str
    identifier: int


DUMMY_MODELS = [
    Model(
        platform="huggingface",
        platform_identifier="distilbert-base-uncased-finetuned-sst-2-english",
        description="",
        name="distilbert-base-uncased-finetuned-sst-2-english",
        same_as="https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english",
        identifier=1,
    ),
    Model(
        platform="huggingface",
        platform_identifier="kinit/slovakbert-sentiment-twitter",
        description="",
        name="kinit/slovakbert-sentiment-twitter",
        same_as="https://huggingface.co/kinit/slovakbert-sentiment-twitter",
        identifier=2,
    ),
    Model(
        platform="huggingface",
        platform_identifier="j-hartmann/sentiment-roberta-large-english-3-classes",
        description="",
        name="j-hartmann/sentiment-roberta-large-english-3-classes",
        same_as="https://huggingface.co/j-hartmann/sentiment-roberta-large-english-3-classes",
        identifier=3,
    ),
]


def get_dummy_models() -> list[Model]:
    return DUMMY_MODELS


def get_dummy_model(id: int) -> Model | None:
    for model in DUMMY_MODELS:
        if model.identifier == id:
            return model
    return None


def get_dummy_model_count():
    return len(DUMMY_MODELS)
