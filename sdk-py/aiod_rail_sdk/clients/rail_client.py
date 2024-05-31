import os

from aiod_rail_sdk.clients.dataset_client import DatasetClient
from aiod_rail_sdk.clients.experiment_client import ExperimentClient
from aiod_rail_sdk.clients.experiment_template_client import ExperimentTemplateClient
from aiod_rail_sdk.configuration import Configuration


class RailClient:
    """
    A class to  work with AIOD-RAIL.
    This class serves as SDK for utilizing python to access AIOD-RAIL.
    It provides properties to access different endpoints.

    Properties:
        experiments (Experiment): Provides access to aiod_rail_sdk Experiment.
        experiments_templates (ExperimentsTemplates): Provides access to aiod_rail_sdk ExperimentTemplate.
        datasets (Datasets): Provides access to aiod_rail_sdk Dataset.

    """

    def __init__(self, config: Configuration, api_key: str | None = None) -> None:
        """
        Creates RailClient to access SDK.
        Args:
            config (Configuration): Configuration specified by host, to which SDK will send requests.
            api_key (str): API-KEY generated in Profile section after singing in AI on Demand.
        Returns:
            None
        """
        self.config = config
        self.config.api_key["APIKeyHeader"] = api_key or os.getenv("AIOD_RAIL_API_KEY")
        self._experiments: ExperimentClient = None
        self._experiments_templates: ExperimentTemplateClient = None
        self._datasets: DatasetClient = None

    @property
    def experiments(self):
        if self._experiments is None:
            self._experiments = ExperimentClient(self.config)
        return self._experiments

    @property
    def experiments_templates(self):
        if self._experiments_templates is None:
            self._experiments_templates = ExperimentTemplateClient(self.config)
        return self._experiments_templates

    @property
    def datasets(self):
        if self._datasets is None:
            self._datasets = DatasetClient(self.config)
        return self._datasets
