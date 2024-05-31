import json
from pathlib import Path
from typing import Optional

from aiod_rail_sdk import (
    ApiClient,
    Configuration,
    ExperimentCreate,
    ExperimentResponse,
    ExperimentRunResponse,
    ExperimentRunsApi,
    ExperimentsApi,
)


class ExperimentClient:
    def __init__(self, config: Configuration):
        self._config = config

    def create_experiment(self, experiment) -> ExperimentResponse:
        """
        Creates experiment from specified experiment file.
        Args:
            experiment (dict): Experiment described in json file.

        Returns:
            ExperimentResponse: Experiment created from given template.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)
            json_data = json.dumps(experiment)
            experiment_create_instance = ExperimentCreate.from_json(json_data)
            try:
                api_response = api_instance.create_experiment_v1_experiments_post(
                    experiment_create_instance
                )
                return api_response

            except Exception as e:
                raise e

    def run_experiment(self, id: str) -> ExperimentRunResponse:
        """
        Runs specified experiment.
        Args:
            id (str): ID of experiment to be run.

        Returns:
            ExperimentRunResponse: Experiment run of given experiment.

        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)
            try:
                api_response = (
                    api_instance.execute_experiment_run_v1_experiments_id_execute_get(
                        id
                    )
                )
                return api_response

            except Exception as e:
                raise e

    def count(
        self,
        query: str = "",
        mine: Optional[bool] = None,
        archived: Optional[bool] = None,
        public: Optional[bool] = None,
    ) -> int:
        """
        Gets experiment count.
        Args:
            query (str, optional): Query used to filter experiments. Defaults to empty string, which means that by default, it's not used.
            mine (bool, optional): If own personal experiments should be counted or the opposite. Defaults to None.
            archived (bool, optional): If archived experiments should be counted or the opposite. Defaults to None.
            public (bool, optional): If experiment templates flagged as public should be counted or the opposite. Defaults to None.

        Returns:
            int: Number of experiments.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)
            try:
                api_response = (
                    api_instance.get_experiments_count_v1_count_experiments_get(
                        query=query, mine=mine, archived=archived, public=public
                    )
                )
                return api_response
            except Exception as e:
                raise e

    def get(
        self,
        query: str = "",
        mine: Optional[bool] = None,
        archived: Optional[bool] = None,
        public: Optional[bool] = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[ExperimentResponse]:
        """
        Gets experiments in specified range.
        Args:
            query (str, optional): Query used to filter experiments. Defaults to empty string, which means that by default, it's not used.
            mine (bool, optional): If own personal experiments should be included or the opposite. Defaults to None.
            archived (bool, optional): If archived experiments should be listed or the opposite. Defaults to None.
            public (bool, optional): If experiment templates flagged as public should be listed or the opposite. Defaults to None.
            offset (int, optional): Starting index of experiment range from which to retrieve. Defaults to 0.
            limit (int, optional): Ending index of experiment range to which to retrieve. Defaults to 100.

        Returns:
            list[ExperimentResponse]: The list of experiments.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)
            try:
                api_response = api_instance.get_experiments_v1_experiments_get(
                    query=query,
                    mine=mine,
                    archived=archived,
                    public=public,
                    offset=offset,
                    limit=limit,
                )
                return api_response
            except Exception as e:
                raise e

    def get_by_id(self, id: str) -> ExperimentResponse:
        """
        Gets specific experiment by its ID.
        Args:
            id (str): ID of experiment to be retrieved.

        Returns:
            ExperimentResponse: Experiment specified by given ID.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)
            try:
                api_response = api_instance.get_experiment_v1_experiments_id_get(id)
                return api_response
            except Exception as e:
                raise e

    def archive(self, id: str, archive: bool = False) -> None:
        """
        Archives specific experiment specified by ID.
        Args:
            id (str): ID of experiment to be archived.
            archive (bool): If experiment should be archived or un-archived. Defaults to False.
        Returns:
            None.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)

            try:
                api_instance.archive_experiment_v1_experiments_id_archive_patch(
                    id=id, archive=archive
                )
            except Exception as e:
                raise e

    def update(self, id: str, experiment: dict) -> ExperimentResponse:
        """
        Updates specific experiment.
        Args:
            id (str): ID of experiment to be updated.
            experiment (dict): Experiment template described in json file.

        Returns:
            ExperimentResponse: Updated Experiment by given ID.
        """
        json_data = json.dumps(experiment)

        experiment_create_instance = ExperimentCreate.from_json(json_data)

        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)

            try:
                api_response = api_instance.update_experiment_v1_experiments_id_put(
                    id=id, experiment_create=experiment_create_instance
                )
                return api_response
            except Exception as e:
                raise e

    def delete(self, id: str) -> None:
        """
        Delete specific experiment specified by ID.
        Args:
            id (str): ID of experiment to be removed.
        Returns:
            None.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)

            try:
                api_instance.delete_experiment_v1_experiments_id_delete(id=id)
            except Exception as e:
                raise e

    def get_experiment_runs(
        self, id: str, offset: int = 0, limit: int = 100
    ) -> list[ExperimentRunResponse]:
        """
        Gets runs of specified experiment in selected range.
        Args:
            id (str): ID of experiment from which runs will be fetched.
            offset (int, optional): Starting index of experiment run range from which to retrieve. Defaults to 0.
            limit (int, optional): Ending index of experiment run range to which to retrieve. Defaults to 100.
        Returns:
            None.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)

            try:
                api_response = api_instance.get_experiment_runs_of_experiment_v1_experiments_id_runs_get(
                    id=id, offset=offset, limit=limit
                )
                return api_response
            except Exception as e:
                raise e

    def get_experiment_runs_count(self, id: str) -> int:
        """
        Gets count of experiment runs.
        Args:
            id (str): ID of experiment from which count of runs will be fetched.
        Returns:
            int: Number of experiment runs of selected experiment.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)

            try:
                api_response = api_instance.get_experiment_runs_of_experiment_count_v1_count_experiments_id_runs_get(
                    id=id
                )
                return api_response
            except Exception as e:
                raise e

    def delete_experiment_run(self, id: str) -> None:
        """
        Deletes experiment run.
        Args:
            id (str): ID of experiment run to be deleted.
        Returns:
            None.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentRunsApi(api_client)

            try:
                api_instance.delete_experiment_run_v1_experiment_runs_id_delete(id)
            except Exception as e:
                raise e

    def download_experiment_run(self, id: str, filepath: str, to_dir: str) -> None:
        """
        Downloads experiment run.
        Args:
            id (str): ID of experiment run to be downloaded.
            filepath (str): File to be downloaded.
            to_dir (Path): Local directory path to which run will be downloaded.
        Returns:
            None.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentRunsApi(api_client)

            try:
                data = api_instance.download_file_from_experiment_run_v1_experiment_runs_id_files_download_get(
                    id=id, filepath=filepath
                )
            except Exception as e:
                raise e

        local_file_path = Path(to_dir) / Path(filepath)
        local_file_path.parent.mkdir(parents=True, exist_ok=True)
        with local_file_path.open("w") as f:
            f.write(data)

    def logs_experiment_run(self, id: str) -> str:
        """
        Gets logs of experiment run.
        Args:
            id (str): ID of experiment run of which logs will be fetched.
        Returns:
            str: Logs of experiment run.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentRunsApi(api_client)

            try:
                api_response = (
                    api_instance.get_experiment_run_logs_v1_experiment_runs_id_logs_get(
                        id=id
                    )
                )
                return api_response
            except Exception as e:
                raise e
