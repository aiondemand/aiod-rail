from beanie import Document


class Experiment(Document):
    dataset_ids: list[str]
    publication_ids: list[str]

    class Settings:
        name = "experiments"
