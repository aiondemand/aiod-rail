from aiod_rail_sdk import ApiClient, AssetsApi, Configuration, Dataset


class DatasetClient:
    def __init__(self, config: Configuration):
        self._config = config

    def count(self) -> int:
        """
        Get total number of datasets.

        Args:
            None

        Returns:
            int: Number of datasets.
        """
        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
            try:
                api_response = (
                    api_instance.get_datasets_count_v1_assets_counts_datasets_get()
                )
                return api_response
            except Exception as e:
                raise e

    def get(self, offset: int = 0, limit: int = 100) -> list[Dataset]:
        """
        Retrieves datasets in specified range.

        Args:
            offset (int, optional): Starting index of dataset range from which to retrieve. Defaults to 0.
            limit (int, optional): Ending index of dataset range to which to retrieve. Defaults to 100.

        Returns:
           list[Dataset]: The list of datasets.
        """
        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
            try:
                api_response = api_instance.get_datasets_v1_assets_datasets_get(
                    offset=offset, limit=limit
                )
                return api_response
            except Exception as e:
                raise e

    def get_by_id(self, id: int) -> Dataset:
        """
        Retrieves dataset specified by its ID.

        Args:
            id (int): Index of dataset in database.

        Returns:
             Dataset: The dataset corresponding to the given ID.
        """
        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
            try:
                api_response = api_instance.get_dataset_v1_assets_datasets_id_get(id)
                return api_response
            except Exception as e:
                raise e
