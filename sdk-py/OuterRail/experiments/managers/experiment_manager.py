from typing import Optional, List, Dict

from OuterRail import Configuration, ApiClient, ExperimentsApi, Experiment


class ExperimentManager:

    """
    AIoD - RAIL
    ExperimentManager class

    Class aggregating methods for operating on multiple experiments.
    """

    def __init__(self, client_config: Configuration):
        """
        Initializes a new ExperimentManager.

        Args:
            client_config: (Configuration): Instance of Configuration class.

        Returns:
            ExperimentManager: Initialized ExperimentManager.

        Examples:
            >>> config = Configuration(...)
            >>> ExperimentManager(config)
            ExperimentManager
        """

        self._config = client_config

    def count(self,
              query: str = "",
              mine: Optional[bool] = None,
              archived: Optional[bool] = None,
              public: Optional[bool] = None
              ) -> int:
        """
        Counts the number of experiments based on filters specified in Args.

        Args:
            query (str, optional): Query used to filter experiments. Defaults to empty string, which means that by default, it's not used.
            mine (bool, optional): If own personal experiments should be counted or the opposite. Defaults to None.
            archived (bool, optional): If archived experiments should be counted or the opposite. Defaults to None.
            public (bool, optional): If experiment templates flagged as public should be counted or the opposite. Defaults to None.

        Returns:
            int: Number of experiments.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> experiment_manager =  ExperimentManager(...)
            >>> experiment_manager.count(query="Tutorial", mine=True, archived=True)
            ExperimentTemplate
        """

        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)
        try:
            api_response = api_instance.get_experiments_count_v1_count_experiments_get(
                query=query, mine=mine, archived=archived, public=public
                )
            return api_response
        except Exception as e:
            raise e


    def get(self, query: str = "", mine: Optional[bool] = None, archived: Optional[bool] = None,
            public: Optional[bool] = None, offset: int = 0, limit: int = 100) -> List[Experiment]:
        """
        Retrieves a lis of experiments based on specific filters.

        Args:
            query (str, optional): Query used to filter experiments. Defaults to empty string, which means that by default, it's not used.
            mine (bool, optional): If own personal experiments should be included or the opposite. Defaults to None.
            archived (bool, optional): If archived experiments should be listed or the opposite. Defaults to None.
            public (bool, optional): If experiment templates flagged as public should be listed or the opposite. Defaults to None.
            offset (int, optional): Starting index of experiment range from which to retrieve. Defaults to 0.
            limit (int, optional): Ending index of experiment range to which to retrieve. Defaults to 100.

        Returns:
            list[Experiment]: The list of experiments.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> experiment_manager =  ExperimentManager(...)
            >>> experiment_manager.get()
            List[Experiment]
            >>> len(experiment_manager.get(archived=False, public=True, limit=1000))
            1000
            >>> template_manager.get(query="Tutorial")
            List[Experiment] # only experimenets that contain word "Tutorial" in their name.
        """

        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)
            try:
                api_response = api_instance.get_experiments_v1_experiments_get(
                    query=query, mine=mine, archived=archived, public=public, offset=offset, limit=limit,
                )
                return [Experiment.from_dict(sub_data, self._config) for sub_data in api_response]
            except Exception as e:
                raise e

    def get_by_id(self, id: str) -> Experiment:
        """
        Gets specific experiment by its ID.

        Args:
            id (str): ID of experiment to be retrieved.

        Returns:
            Experiment: Experiment specified by its ID.

        Raises:
            ApiException: In case of a failed HTTP request or failure to retrieve an experiment with given ID.

        Examples:
            >>> experiment_manager =  ExperimentManager(...)
            >>> experiment_manager.get_by_id("6861d3c954d2c02536469a30")
            Experiment
        """

        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)
            try:
                api_response = api_instance.get_experiment_v1_experiments_id_get(id)
                return Experiment.from_dict(api_response, self._config)
            except Exception as e:
                raise e

    def create(self, experiment: Dict) -> Experiment:
        """
        Creates experiment from specified experiment file.
        Args:
            experiment (dict): Experiment described in a dictionary.

        Returns:
            Experiment: Experiment created from given template.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> experiment_dict = {
            >>>     "name": "test123",
            >>>     "description": "321test",
            >>>     "is_public": True,
            >>>     "experiment_template_id": "685151f2d08da970a3a5d6ce",
            >>>     "dataset_ids": ["data_000002AhzqHqOQwQLP0qCRds"],
            >>>     "model_ids": ["mdl_003Csk8QjNfE80c7g6Rt8yVb"],
            >>>     "publication_ids": [],
            >>>     "env_vars": [{"key": "SPLIT_NAME", "value": "PES"}
            >>>     ]
            >>> }
            >>> experiment_manager =  ExperimentManager(...)
            >>> experiment_manager.create(experiment_dict)
            Experiment # Newly created experiment.
        """

        with ApiClient(self._config) as api_client:
            api_instance = ExperimentsApi(api_client)
            try:
                api_response = api_instance.create_experiment_v1_experiments_post(experiment)
                return Experiment.from_dict(api_response, self._config)
            except Exception as e:
                raise e
