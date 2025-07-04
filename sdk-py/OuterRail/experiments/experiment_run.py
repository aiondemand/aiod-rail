from pathlib import Path
from datetime import datetime
from typing_extensions import Self
from typing import Any, ClassVar, Dict, List, Optional, Set, Union
from pydantic import BaseModel, ConfigDict, StrictBool, StrictFloat, StrictInt, StrictStr

from OuterRail import RunState, Configuration, ApiClient, ExperimentRunsApi

"""
    AIoD - RAIL

    ExperimentRun class. 

    Implementation of class representing a specific experiment run with 
    methods for operating on this run.
"""


class ExperimentRun(BaseModel):

    id: StrictStr
    experiment_id: StrictStr
    retry_count: StrictInt
    is_mine: StrictBool
    is_public: StrictBool
    is_archived: StrictBool
    created_at: datetime
    updated_at: datetime
    state: RunState
    metrics: Dict[str, Union[StrictFloat, StrictInt]]
    __properties: ClassVar[List[str]] = [
        "id", "experiment_id", "created_at", "updated_at", "retry_count", "state", "metrics", "is_public",
        "is_archived", "is_mine"
    ]
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True, protected_namespaces=())

    def delete(self) -> None:
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
            api_instance = ExperimentRunsApi(api_client)
            try:
                api_instance.delete_experiment_run_v1_experiment_runs_id_delete(self.id)
                self._deleted = True
            except Exception as e:
                raise e

    def download_file(self, filepath: str, to_dir: str) -> None:
        """
        Downloads a specific file contained in outputs for the run.

        Args:
            filepath (str): File to be downloaded.
            to_dir (Path): Local directory path to which run will be downloaded.

        Returns:
            None.

         Raises:
             ApiException: In case of a failed HTTP request.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentRunsApi(api_client)

            try:
                data = api_instance.download_file_from_experiment_run_v1_experiment_runs_id_files_download_get(
                    id=self.id, filepath=filepath
                )
            except Exception as e:
                raise e

        local_file_path = Path(to_dir) / Path(filepath)
        local_file_path.parent.mkdir(parents=True, exist_ok=True)
        with local_file_path.open("w") as f:
            f.write(data)

    def logs(self) -> str:
        """
        Fetches the logs of the experiment run.

        Returns:
            str: Logs of experiment run.

         Raises:
             ApiException: In case of a failed HTTP request.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentRunsApi(api_client)
            try:
                api_response = api_instance.get_experiment_run_logs_v1_experiment_runs_id_logs_get(id=self.id)
                return api_response
            except Exception as e:
                raise e

    def _set_config(self, config: Configuration) -> None:
        """
        Sets the configuration  required for API calls.

        Args:
        config (:obj:`Configuration`): The api configuration.

        Returns:
            None:
        """
        self._config = config

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]], config: Configuration = None) -> Optional[Self]:
        """
        Creates an instance of an ExperimentRun from dict.

        Args:
            obj (Optional[Dict[str, Any]]): Obj representing the experiment run in either a dictionary or
            an already existing instance.
            config (:obj:`Configuration`, optional): The configuration for api calls. Defaults to None.

        Returns:
            None: If input arg "obj" is None.
            ExperimentRun: In successful conversion from dict.
        """
        if obj is None:
            return None

        _obj = cls.model_validate(obj)
        if config is not None:
            _obj._set_config(config)
        return _obj
