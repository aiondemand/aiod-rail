import json

import aiod_rail_sdk


class Experiments:
    def __init__(self, config: aiod_rail_sdk.Configuration):
        self._config = config

    def create_experiment(self, file) -> aiod_rail_sdk.ExperimentResponse:
        """
        Creates experiment from specified experiment template.
        Args:
            file (dict): Experiment template described in json file.

        Returns:
            aiod_rail_sdk.ExperimentResponse: Experiment created from given template.
        """
        with aiod_rail_sdk.ApiClient(self._config) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
            json_data = json.dumps(file)
            experiment_create_instance = aiod_rail_sdk.ExperimentCreate.from_json(
                json_data
            )
            try:
                api_response = api_instance.create_experiment_v1_experiments_post(
                    experiment_create_instance
                )
                return api_response

            except Exception as e:
                raise e

    def run_experiment(self, id: str) -> aiod_rail_sdk.ExperimentRunResponse:
        """
        Runs specified experiment.
        Args:
            id (str): ID of experiment to be run.

        Returns:
            aiod_rail_sdk.ExperimentRunResponse: Experiment run of given experiment.

        """
        with aiod_rail_sdk.ApiClient(self._config) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
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
        mine: bool = True,
        archived: bool = False,
        public: bool = True,
    ) -> int:
        """
        Gets experiment count.
        Args:
            query (str, optional): Query used to filter experiments. Defaults to empty string, which means that by default, it's not used.
            mine (bool, optional): If own personal experiments should be counted. Defaults to True.
            archived (bool, optional): If archived experiments should be counted. Defaults to False.
            public (bool, optional): If experiment templates flagged as public should be counted. Defaults to True.

        Returns:
            int: Number of experiments.
        """
        with aiod_rail_sdk.ApiClient(self._config) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
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
        mine: bool = True,
        archived: bool = False,
        public: bool = True,
        offset: int = 0,
        limit: int = 100,
    ) -> list[aiod_rail_sdk.ExperimentResponse]:
        """
        Gets experiments in specified range.
        Args:
            query (str, optional): Query used to filter experiments. Defaults to empty string, which means that by default, it's not used.
            mine (bool, optional): If own personal experiments should be included. Defaults to True.
            archived (bool, optional): If archived experiments should be listed. Defaults to False.
            public (bool, optional): If experiment templates flagged as public should be listed. Defaults to True.
            offset (int, optional): Starting index of experiment range from which to retrieve. Defaults to 0.
            limit (int, optional): Ending index of experiment range to which to retrieve. Defaults to 100.

        Returns:
            list[aiod_rail_sdk.ExperimentResponse]: The list of experiments.
        """
        with aiod_rail_sdk.ApiClient(self._config) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
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

    def get_by_id(self, id: str) -> aiod_rail_sdk.ExperimentResponse:
        """
        Gets specific experiment by its ID.
        Args:
            id (str): ID of experiment to be retrieved.

        Returns:
            aiod_rail_sdk.ExperimentResponse: Experiment specified by given ID.
        """
        with aiod_rail_sdk.ApiClient(self._config) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
            try:
                api_response = api_instance.get_experiment_v1_experiments_id_get(id)
                return api_response
            except Exception as e:
                raise e

    def archive(self, id: str, archived: bool = False) -> None:
        """
        Archives specific experiment specified by ID.
        Args:
            id (str): ID of experiment to be archived.
            archived (bool): If experiment should be archived or un-archived. Defaults to False.
        Returns:
            None.
        """
        with aiod_rail_sdk.ApiClient(self._config) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)

            try:
                api_instance.archive_experiment_v1_experiments_id_archive_patch(
                    id=id, archived=archived
                )
            except Exception as e:
                raise e

    def update(self, id: str, file: dict) -> aiod_rail_sdk.ExperimentResponse:
        """
        Updates specific experiment.
        Args:
            id (str): ID of experiment to be updated.
            file (dict): Experiment template described in json file.

        Returns:
            aiod_rail_sdk.ExperimentResponse: Updated Experiment by given ID.
        """
        json_data = json.dumps(file)

        experiment_create_instance = aiod_rail_sdk.ExperimentCreate.from_json(json_data)

        with aiod_rail_sdk.ApiClient(self._config) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)

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
        with aiod_rail_sdk.ApiClient(self._config) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)

            try:
                api_instance.delete_experiment_v1_experiments_id_delete(id=id)
            except Exception as e:
                raise e

    def get_experiments_run(
        self, id: str, offset: int = 0, limit: int = 100
    ) -> list[aiod_rail_sdk.ExperimentRunResponse]:
        """
        Gets runs of specified experiment in selected range.
        Args:
            id (str): ID of experiment from which runs will be fetched.
            offset (int, optional): Starting index of experiment run range from which to retrieve. Defaults to 0.
            limit (int, optional): Ending index of experiment run range to which to retrieve. Defaults to 100.
        Returns:
            None.
        """
        with aiod_rail_sdk.ApiClient(self._config) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)

            try:
                # Get Experiment Runs Of Experiment
                api_response = api_instance.get_experiment_runs_of_experiment_v1_experiments_id_runs_get(
                    id=id, offset=offset, limit=limit
                )
                return api_response
            except Exception as e:
                raise e

    def get_experiments_run_count(self, id: str) -> int:
        """
        Gets count of experiments runs.
        Args:
            id (str): ID of experiment from which count of runs will be fetched.
        Returns:
            int: Number of experiments runs of selected experiment.
        """
        with aiod_rail_sdk.ApiClient(self._config) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)

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
        with aiod_rail_sdk.ApiClient(self._config) as api_client:
            api_instance = aiod_rail_sdk.ExperimentRunsApi(api_client)

            try:
                api_instance.delete_experiment_run_v1_experiment_runs_id_delete(id)
            except Exception as e:
                raise e

    def download_experiment_run(self, id: str, filepath: str) -> None:
        """
        Downloads experiment run.
        Args:
            id (str): ID of experiment run to be downloaded.
            filepath (str): Local path to which run will be downloaded.
        Returns:
            None.
        """
        with aiod_rail_sdk.ApiClient(self._config) as api_client:
            api_instance = aiod_rail_sdk.ExperimentRunsApi(api_client)

            try:
                api_instance.download_file_from_experiment_run_v1_experiment_runs_id_files_download_get(
                    id=id, filepath=filepath
                )
            except Exception as e:
                raise e

    def logs_experiment_run(self, id: str) -> str:
        """
        Gets logs of experiment run.
        Args:
            id (str): ID of experiment run of which logs will be fetched.
        Returns:
            None.
        """
        with aiod_rail_sdk.ApiClient(self._config) as api_client:
            api_instance = aiod_rail_sdk.ExperimentRunsApi(api_client)

            try:
                api_response = (
                    api_instance.get_experiment_run_logs_v1_experiment_runs_id_logs_get(
                        id=id
                    )
                )
                return api_response
            except Exception as e:
                raise e
