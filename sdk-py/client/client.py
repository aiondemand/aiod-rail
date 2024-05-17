import aiod_rail_sdk
from .experiment_client import Experiments
from .experiment_template_client import ExperimentsTemplates
from .dataset_client import Datasets

class RailClient:
    def __init__(self, configuration: aiod_rail_sdk.Configuration) -> None:
        self.config = configuration
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

    

