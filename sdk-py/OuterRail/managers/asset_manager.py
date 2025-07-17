from typing import List

from OuterRail import Configuration, ApiClient, AssetsApi, Dataset

from aiod_rail_sdk import Publication


class AssetManager:
    """
    AIoD - RAIL
    AssetManager class

    Class containing methods that operate on simpler assets such as: models, datasets, publications, etc..
    """

    def __init__(self, client_config: Configuration):
        """
        Initializes a new ExperimentRunManager.

        Args:
            client_config: (Configuration): Instance of Configuration class.

        Returns:
            AssetManager: Initialized AssetManager.

        Examples:
            >>> config = Configuration(...)
            >>> AssetManager(config)
            AssetManager
        """

        self._config = client_config

    def get_datasets(self, query: str = None, offset: int = 0, limit: int = 100) -> List[Dataset]:
        """
        Retrieves a list of available datasets.

        Args:
            query (str, optional): Search string used to filter datasets. Defaults to empty string,
            which means that by default, it's not used.
            offset (int, optional): Starting index of from which to retrieve. Defaults to 0.
            limit (int, optional): How many items to retrieve. Defaults to 100.

        Returns:
            List[Dataset]: The list of datasets.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
        """

        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
        try:
            if query is None:
                api_response = api_instance.get_datasets(offset=offset, limit=limit)
            else:
                api_response = api_instance.query_get_datasets(query=query, offset=offset, limit=limit)
            return [Dataset.from_dict(sub_data, self._config) for sub_data in api_response]
        except Exception as e:
            raise e

    def count_publications(self, query: str = None) -> int:
        """
        Counts the number of publications.

        Args:
            query: (Optional[str]): Count only publications that contain a string given in this arg.

        Returns:
            int: Number of publications.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> asset_manager =  AssetManager(...)
            >>> asset_manager.count_publications()
            4321
            >>> asset_manager.count_publications(query="CNNs")
            1234 # count of publications that contain the phrase "CNNs"
        """

        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
        try:
            if query is None:
                api_response = api_instance.count_publications()
            else:
                api_response = api_instance.query_count_publications(query=query)
            return api_response
        except Exception as e:
            raise e

    def get_publications(self, query: str = None, offset: int = 0, limit: int = 100) -> List[Publication]:
        """
        Retrieves a list of publications.

        Args:
            query (str, optional): Search string used to filter publications. Defaults to empty string,
            which means that by default, it's not used.
            offset (int, optional): Starting index of experiment range from which to retrieve. Defaults to 0.
            limit (int, optional): Ending index of experiment range to which to retrieve. Defaults to 100.

        Returns:
            List[Experiment]: The list of experiments.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
        """

        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
        try:
            if query is None:
                api_response = api_instance.get_publications(offset=offset, limit=limit)
            else:
                api_response = api_instance.query_get_publications(query=query, offset=offset, limit=limit)
            return api_response
        except Exception as e:
            raise e
