from OuterRail import Configuration, ApiClient, ExperimentRun, ExperimentRunsApi



class ExperimentRunManager:

    """
    AIoD - RAIL
    ExperimentRunManager class

    Class aggregating methods for operating on multiple experiment runs and which are not restricted to a specific
    experiment.
    """

    def __init__(self, client_config: Configuration):
        """
        Initializes a new ExperimentRunManager.

        Args:
            client_config: (Configuration): Instance of Configuration class.

        Returns:
            ExperimentRunManager: Initialized ExperimentRunManager.

        Examples:
            >>> config = Configuration(...)
            >>> ExperimentRunManager(config)
            ExperimentRunManager
        """

        self._config = client_config

    def get_by_id(self, id: str) -> ExperimentRun:
        """
        Gets specific experiment run by its ID.

        Args:
            id (str): ID of an experiment run to be retrieved.

        Returns:
            ExperimentRun: Experiment run specified by its ID.

        Raises:
            ApiException: In case of a failed HTTP request or failure to retrieve an experiment with given ID.

        Examples:
            >>> run_manager =  ExperimentRunManager(...)
            >>> run_manager.get_by_id("6861d3c954d2c02536469a30")
            ExperimentRun
        """

        with ApiClient(self._config) as api_client:
            api_instance = ExperimentRunsApi(api_client)
            try:
                api_response = api_instance.get_run_by_id(id)
                return ExperimentRun.from_dict(api_response, self._config)
            except Exception as e:
                raise e
