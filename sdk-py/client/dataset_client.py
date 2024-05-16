import aiod_rail_sdk

class Datasets:
    # TODO change to client.py strategy
    def __init__(self, host='http://localhost/api') -> None:
        self._host=host
        self._configuration = aiod_rail_sdk.Configuration(host=self._host)

    def count(self):
        """
            Get total number of datasets
            
            Args:
                None

            Returns:
                int: Total number of datasets
        """
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
                api_instance = aiod_rail_sdk.AssetsApi(api_client)
                try:
                    api_response = api_instance.get_datasets_count_v1_assets_counts_datasets_get()
                    return api_response
                except Exception as e:
                    raise (f'Exception {e}')

    def get(self, offset: int = 0, limit: int = 100) -> list:
        """
            Retrieves datasets in specified range

            Args:
                offset (int): Starting index of dataset range from which to retrieve
                limit (int): Ending index of dataset range to which to retrieve

            Returns:
                List[Dataset]: List of aiod_rail_sdk.models.dataset.Dataset classes
        """
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
            api_instance = aiod_rail_sdk.AssetsApi(api_client)
            try:
                api_response = api_instance.get_datasets_v1_assets_datasets_get(offset=offset, limit=limit)
                return api_response
            except Exception as e:
                raise (f'Exception {e}')
    
    def get_by_id(self, id: int):
        """
            Retrieves dataset specified by it's id

            Args:
                id (int): Index of dataset in database

            Returns:
                 Dataset: aiod_rail_sdk.models.dataset.Dataset class
        """
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
            api_instance = aiod_rail_sdk.AssetsApi(api_client)
            try:
                api_response = api_instance.get_dataset_v1_assets_datasets_id_get(id)
                return api_response
            except Exception as e:
                raise (f'Exception {e}')