import aiod_rail_sdk

class Datasets:
    def __init__(self, client_config: aiod_rail_sdk.Configuration):
        self._configuration = client_config

    def count(self) -> int:
        """
            Get total number of datasets.
            
            Args:
                None

            Returns:
                int: Number of datasets.
        """
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
                api_instance = aiod_rail_sdk.AssetsApi(api_client)
                try:
                    api_response = api_instance.get_datasets_count_v1_assets_counts_datasets_get()
                    return api_response
                except Exception as e:
                    raise (f'Exception {e}')

    def get(self, offset: int = 0, limit: int = 100) -> list[aiod_rail_sdk.Dataset]:
        """
            Retrieves datasets in specified range.

            Args:
                offset (int, optional): Starting index of dataset range from which to retrieve. Defaults to 0.
                limit (int, optional): Ending index of dataset range to which to retrieve. Defaults to 100.

            Returns:
               list[aiod_rail_sdk.Dataset]: The list of datasets.
        """
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
            api_instance = aiod_rail_sdk.AssetsApi(api_client)
            try:
                api_response = api_instance.get_datasets_v1_assets_datasets_get(offset=offset, limit=limit)
                return api_response
            except Exception as e:
                raise (f'Exception {e}')
    
    def get_by_id(self, id: int) -> aiod_rail_sdk.Dataset:
        """
            Retrieves dataset specified by it's ID.

            Args:
                id (int): Index of dataset in database.

            Returns:
                 aiod_rail_sdk.Dataset: The dataset corresponding to the given ID.
        """
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
            api_instance = aiod_rail_sdk.AssetsApi(api_client)
            try:
                api_response = api_instance.get_dataset_v1_assets_datasets_id_get(id)
                return api_response
            except Exception as e:
                raise (f'Exception {e}')