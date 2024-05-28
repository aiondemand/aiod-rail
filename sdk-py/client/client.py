import aiod_rail_sdk
from .experiment_client import Experiments
from .experiment_template_client import ExperimentsTemplates
from .dataset_client import Datasets

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
    def __init__(self, 
                 configuration: aiod_rail_sdk.Configuration, 
                 api_key) -> None:
        """
            Creates RailClient to access SDK.
            Args:
                config (aiod_rail_sdk.Configuration): Configuration specified by host, to which SDK will send requests.
                api_key (str): API-KEY generated in Profile section after singing in AI on Demand.
            Returns:
                None
        """
        self.config = configuration
        self.config.api_key['APIKeyHeader'] = api_key
        self._experiments: Experiments = None
        self._expetiments_templates: ExperimentsTemplates = None
        self._datasets: Datasets = None

    @property
    def experiments(self):
        if self._experiments is None:
            self._experiments = Experiments(self.config)
        return self._experiments

    @property
    def experiments_templates(self):
        if self._expetiments_templates is None:
            self._experiments_templates = ExperimentsTemplates(self.config)
        return self._experiments_templates
    
    @property
    def datasets(self):
        if self._datasets is None:
            self._datasets = Datasets(self.config)
        return self._datasets

    

