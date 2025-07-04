from datetime import datetime
from typing_extensions import Self
from typing import Any, ClassVar, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, StrictBool, StrictStr

from OuterRail.experiments.experiment_run import ExperimentRun
from OuterRail import EnvironmentVar, Configuration, ApiClient, ExperimentsApi

"""
    AIoD - RAIL

    Experiment class. 
    
    Implementation of class representing an instance of experiment and methods
    operating with this instance.
"""


class Experiment(BaseModel):
    id: StrictStr
    name: StrictStr
    description: StrictStr
    experiment_template_id: StrictStr
    is_mine: StrictBool
    is_public: StrictBool
    is_archived: StrictBool
    created_at: datetime
    updated_at: datetime
    model_ids: List[StrictStr]
    dataset_ids: List[StrictStr]
    env_vars: List[EnvironmentVar]
    publication_ids: Optional[List[StrictStr]] = None
    __properties: ClassVar[List[str]] = [
        "name", "description", "is_public", "experiment_template_id", "dataset_ids", "model_ids", "publication_ids",
        "env_vars", "id", "created_at", "updated_at", "is_archived", "is_mine"
    ]
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True, protected_namespaces=())

    def archive(self, archive: bool = False) -> None:
        """
        Archives specific experiment template specified by ID.

        Args:
            archive (bool): If experiment should be archived or un-archived. Defaults to False.
        Returns:
            None.

        Raises:
            ApiException: In case of a failed HTTP request.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)
            try:
                api_instance.archive_experiment_v1_experiments_id_archive_patch(id=self.id, archive=archive)
                self.is_archived = archive
            except Exception as e:
                raise e

    def update(self, experiment: dict) -> Self:
        """
        Updates the experiment.

        Args:
            experiment (dict): Dictionary containing updated experiment specification.

        Returns:
            Experiment: Updated Experiment.

        Raises:
            ApiException: In case of a failed HTTP request.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)
            try:
                api_response = api_instance.update_experiment_v1_experiments_id_put(
                    id=self.id, experiment_create=experiment
                )
                self.__dict__.update(api_response)
                return self
            except Exception as e:
                raise e

    def delete(self) -> None:
        """
        Delete specific experiment specified by ID.

        Returns:
            None.

        Raises:
            ApiException: In case of a failed HTTP request.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)
            try:
                api_instance.delete_experiment_v1_experiments_id_delete(id=self.id)
                self._deleted = True
            except Exception as e:
                raise e

    def _set_config(self, config: Configuration) -> None:
        """
        Sets the configuration of the experiment template required for API calls.

        Args:
            config (:obj:`Configuration`): The api configuration.

        Returns:
            None:
        """
        self._config = config

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]], config: Configuration = None) -> Optional[Self]:
        """
        Create an instance of ExperimentRunResponse from a dict

        Args:
            obj (Optional[Dict[str, Any]]): Obj representing the experiment in either a dictionary or
            an already existing instance.
            config (:obj:`Configuration`, optional): The api configuration. Defaults to None.

        Returns:
            None: If input arg "obj" is None.
            Experiment: In successful conversion from dict.
        """
        if obj is None:
            return None
        _obj = cls.model_validate(obj)
        if config is not None:
            _obj._set_config(config)
        return _obj

    def count_runs(self) -> int:
        """
        Counts the number of runs of an experiment.

        Returns:
            int: Number of experiment runs of selected experiment.

        Raises:
            ApiException: In case of a failed HTTP request.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)
            try:
                api_response = api_instance.get_experiment_runs_of_experiment_count_v1_count_experiments_id_runs_get(
                    id=self.id
                )
                return api_response
            except Exception as e:
                raise e

    def get_runs(self, offset: int = 0, limit: int = 100) -> List[ExperimentRun]:
        """
        Gets runs of specified experiment in selected range.

        Args:
            offset (int, optional): Starting index of experiment run range from which to retrieve. Defaults to 0.
            limit (int, optional): Ending index of experiment run range to which to retrieve. Defaults to 100.

        Returns:
            None.

        Raises:
            ApiException: In case of a failed HTTP request.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)
            try:
                api_response = api_instance.get_experiment_runs_of_experiment_v1_experiments_id_runs_get(
                    id=self.id, offset=offset, limit=limit
                )
                return [ExperimentRun.from_dict(sub_data, self._config) for sub_data in api_response]
            except Exception as e:
                raise e


    def run(self) -> ExperimentRun:
        """
        Runs an experiment.

        Returns:
            ExperimentRun: Instance of the experiment run.

        Raises:
            ApiException: In case of a failed HTTP request.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)
            try:
                api_response = api_instance.execute_experiment_run_v1_experiments_id_execute_get(self.id)
                return ExperimentRun.from_dict(api_response, self._config)
            except Exception as e:
                raise e
