from beanie import Document


class Experiment(Document):
    title: str
    description: str
    dataset_ids: list[str]
    publication_ids: list[str]

    class Settings:
        name = "experiments"
