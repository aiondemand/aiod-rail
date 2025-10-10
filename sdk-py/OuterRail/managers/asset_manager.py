from typing import List, Dict

from OuterRail import Configuration
from OuterRail import ApiClient, AssetsApi, Dataset, Platform, Publication, Model



class AssetManager:
    """
    AIoD - RAIL
    AssetManager class

    Class containing methods that operate on simpler assets such as: models, datasets, publications, etc..
    """

    def __init__(self, api_config: Configuration):
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

        self._config = api_config

    def count_datasets(self, query: str = None) -> int:
        """
        Counts the number of datasets.

        Args:
            query: (Optional[str]): Count only datasets that in their name contain a string given in this arg.

        Returns:
            int: Number of datasets.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> asset_manager =  AssetManager(...)
            >>> asset_manager.count_datasets()
            4321
            >>> asset_manager.count_datasets(query="Image")
            1234 # count of datasets that contain the phrase "Image"
        """

        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
            try:
                if query is None:
                    api_response = api_instance.count_datasets()
                else:
                    api_response = api_instance.query_count_datasets(query=query)
                return api_response
            except Exception as e:
                raise e

    def count_my_datasets(self) -> int:
        """
        Counts the number of datasets of the current user.

        Returns:
            int: Number of datasets.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> asset_manager =  AssetManager(...)
            >>> asset_manager.count_my_datasets()
            123
        """

        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
            try:
                api_response = api_instance.count_my_datasets()
                return api_response
            except Exception as e:
                raise e

    def get_datasets(self, query: str = None, enhanced: bool = False, offset: int = 0, limit: int = 100
                     ) -> List[Dataset]:
        """
        Retrieves a list of available datasets.

        Args:
            query (str, optional): Search string used to filter datasets. Defaults to empty string,
            which means that by default, it's not used.
            enhanced (bool, optional): If true and the query arg is also specified, a semantic search is performed.
            offset (int, optional): Starting index of from which to retrieve. Defaults to 0.
            limit (int, optional): How many items to retrieve. Defaults to 100.

        Returns:
            List[Dataset]: The list of datasets.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> asset_manager = AssetManager(...)
            >>> asset_manager.get_datasets(query="AI", offset=2, limit=10)
            List[Dataset] # 10 datasets that contain the text "AI" in their name
        """

        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
            try:
                if query is None:
                    api_response = api_instance.get_datasets(offset=offset, limit=limit)
                else:
                    api_response = api_instance.query_get_datasets(query=query, enhanced=enhanced,
                                                                   offset=offset, limit=limit)
                return [Dataset.from_dict(sub_data, self._config) for sub_data in api_response]
            except Exception as e:
                raise e

    def get_my_datasets(self, offset: int = 0, limit: int = 100) -> List[Dataset]:
        """
        Retrieves a list of datasets created by the current user.

        Args:
            offset (int, optional): Starting index from which to retrieve. Defaults to 0.
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
                api_response = api_instance.get_my_datasets(offset=offset, limit=limit)
                return [Dataset.from_dict(sub_data, self._config) for sub_data in api_response]
            except Exception as e:
                raise e


    def get_dataset_by_id(self, id: str) -> Dataset:
        """
        Retrieves dataset specified by its ID.

        Args:
            id (str): Unique identifier of dataset in database.

        Returns:
             Dataset: The dataset corresponding to the given ID.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> asset_manager = AssetManager(...)
            >>> asset_manager.get_dataset_by_id(id="data_000002AhzqHqOQwQLP0qCRds")
            Dataset
        """

        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
            try:
                api_response = api_instance.get_dataset_by_id(id)
                return Dataset.from_dict(api_response, self._config)
            except Exception as e:
                raise e

    # NOT supported on the frontend either, so for now, we comment it out. Needs to run smoothly first.
    # def create_dataset(self, dataset: Dict) -> Dataset:
    #     """
    #     Creates dataset from a given dictionary.
    #
    #     Args:
    #         dataset (dict): dataset described in a dictionary.
    #
    #     Returns:
    #         Dataset: Instance of the created dataset.
    #
    #     Raises:
    #         ApiException: In case of a failed HTTP request.
    #
    #     Examples:
    #         >>> EXAMPLE DATASET DICT
    #         >>> dataset_dict = {
    #         >>> 'ai_asset_identifier': 'string', 'ai_resource_identifier': 'string',
    #         >>> 'aiod_entry': {'date_created': '2022-01-01T15:15:00.000', 'date_modified': '2023-01-01T15:15:00.000',
    #         >>>                'editor': [], 'status': 'published'},
    #         >>> 'alternate_name': ['alias 1', 'alias 2'],
    #         >>> 'application_area': ['Fraud Prevention', 'Voice Assistance', 'Disease Classification'],
    #         >>> 'citation': [],
    #         >>> 'contact': [],
    #         >>> 'creator': [],
    #         >>> 'date_published': '2022-01-01T15:15:00.000',
    #         >>> 'description': {'html': '<p>Text with <strong>html formatting</strong>.</p>',
    #         >>>                 'plain': 'Plain text.'},
    #         >>> 'distribution': [],
    #         >>> 'funder': [],
    #         >>> 'has_part': [],
    #         >>> 'identifier': 'string',
    #         >>> 'industrial_sector': ['Finance', 'eCommerce', 'Healthcare'],
    #         >>> 'is_accessible_for_free': True,
    #         >>> 'is_part_of': [],
    #         >>> 'issn': '20493630',
    #         >>> 'keyword': ['keyword1', 'keyword2'],
    #         >>> 'license': 'https://creativecommons.org/share-your-work/public-domain/cc0/',
    #         >>> 'measurement_technique': 'mass spectrometry',
    #         >>> 'media': [],
    #         >>> 'name': 'The name of this resource',
    #         >>> 'note': [],
    #         >>> 'platform': 'example',
    #         >>> 'platform_resource_identifier': '1',
    #         >>> 'relevant_link': ['https://www.example.com/a_relevant_link', 'https://www.example.com/another_relevant_link'],
    #         >>> 'relevant_resource': [],
    #         >>> 'relevant_to': [],
    #         >>> 'research_area': ['Explainable AI', 'Physical AI'],
    #         >>> 'same_as': 'https://www.example.com/resource/this_resource',
    #         >>> 'scientific_domain': ['Anomaly Detection', 'Voice Recognition', 'Computer Vision.'],
    #         >>> 'size': {'unit': 'Rows', 'value': 100},
    #         >>> 'spatial_coverage': {'address': {'address': 'Wetstraat 170, 1040 Brussel', 'country': 'BEL', 'locality': 'Paris',
    #         >>>                               'postal_code': '1040 AA', 'region': 'California', 'street': 'Wetstraat 170'},
    #         >>>                      'geo': {'elevation_millimeters': 0, 'latitude': 37.42242, 'longitude': -122.08585}},
    #         >>> 'temporal_coverage': '2011/2012',
    #         >>> 'version': '1.1.0'}
    #         >>> asset_manager = AssetManager(...)
    #         >>> asset_manager.create_dataset(dataset_dict)
    #         Dataset # Newly created dataset.
    #     """
    #
    #     with ApiClient(self._config) as api_client:
    #         api_instance = AssetsApi(api_client)
    #         try:
    #             api_response = api_instance.create_dataset(dataset)
    #             return Dataset.from_dict(api_response, self._config)
    #         except Exception as e:
    #             raise e

    def upload_file_to_huggingface(self, id: str, name: str, huggingface_token: str, file_path : str) -> Dataset:
        """
        Uploads a file to Huggingface under the dataset specified by its id.

        Args:
            id (str): The ID of the dataset.
            name (str): The name of the file as it will appear on Huggingface.
            huggingface_token: Authentication token from Huggingface.
            file_path (str): Path to the file to upload.

        Returns:
            Dataset: Dataset under which the file was uploaded.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> asset_manager =  AssetManager(...)
            >>> asset_manager.upload_file_to_huggingface("data_000017VBQZZ7s3cvm7Gx0AnT", "Example Name", "huggingface_token", "path/to/file.txt")
            Dataset
        """

        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
            try:
                with open(file_path, 'rb') as file:
                    file_bytes = file.read()
                api_response = api_instance.dataset_upload_file_to_huggingface(id, name, huggingface_token, file_bytes)
                return Dataset.from_dict(api_response, self._config)
            except Exception as e:
                raise e


    def count_models(self, query: str = None) -> int:
        """
        Counts the number of models.

        Args:
            query: (Optional[str]): Count only models that contain in their name a string given by this arg.

        Returns:
            int: Number of models.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> asset_manager =  AssetManager(...)
            >>> asset_manager.count_models()
            4321
            >>> asset_manager.count_models(query="LLM")
            1234 # count of models that contain the phrase "LLM"
        """

        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
            try:
                if query is None:
                    api_response = api_instance.count_models()
                else:
                    api_response = api_instance.query_count_models(query=query)
                return api_response
            except Exception as e:
                raise e

    def count_my_models(self) -> int:
        """
        Counts the number of models of the current user.

        Returns:
            int: Number of models.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> asset_manager =  AssetManager(...)
            >>> asset_manager.count_my_models()
            123
        """

        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
            try:
                api_response = api_instance.count_my_models()
                return api_response
            except Exception as e:
                raise e

    def get_models(self, query: str = None, offset: int = 0, limit: int = 100) -> List[Model]:
        """
        Retrieves a list of models.

        Args:
            query (str, optional): Search string used to filter models. Defaults to empty string,
            which means that by default, it's not used.
            offset (int, optional): Starting index from which to retrieve. Defaults to 0.
            limit (int, optional): How many items to retrieve. Defaults to 100.

        Returns:
            List[Model]: The list of models.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> asset_manager = AssetManager(...)
            >>> asset_manager.get_models(query="LLM", offset=2, limit=10)
            List[Model] # 10 models that contain the phrase "LLM" in their name
        """

        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
            try:
                if query is None:
                    api_response = api_instance.get_models(offset=offset, limit=limit)
                else:
                    api_response = api_instance.query_get_models(query=query, offset=offset, limit=limit)
                return [Publication.from_dict(sub_data) for sub_data in api_response]
            except Exception as e:
                raise e

    def get_my_models(self, offset: int = 0, limit: int = 100) -> List[Model]:
        """
        Retrieves a list of models created by the current user.

        Args:
            offset (int, optional): Starting index from which to retrieve. Defaults to 0.
            limit (int, optional): How many items to retrieve. Defaults to 100.

        Returns:
            List[Model]: A list of user's models.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> asset_manager = AssetManager(...)
            >>> asset_manager.get_my_models(limit=2)
            List[Model] # first 2 models created by a current user
        """

        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
            try:
                api_response = api_instance.get_my_models(offset=offset, limit=limit)
                return [Model.from_dict(sub_data) for sub_data in api_response]
            except Exception as e:
                raise e

    def get_model_by_id(self, id: str) -> Model:
        """
        Retrieves a model specified by its ID.

        Args:
            id (str): Unique identifier of a model.

        Returns:
             Model: The model corresponding to the given ID.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> asset_manager = AssetManager(...)
            >>> asset_manager.get_model_by_id(id="mdl_000028bcIa2SCbO9aVlIB0Xc")
            Model
        """

        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
            try:
                api_response = api_instance.get_model_by_id(id)
                return Model.from_dict(api_response)
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
            offset (int, optional): Starting index from which to retrieve. Defaults to 0.
            limit (int, optional): How many items to retrieve. Defaults to 100.

        Returns:
            List[Publication]: The list of publications.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> asset_manager = AssetManager(...)
            >>> asset_manager.get_publications(query="AI", offset=2, limit=10)
            List[Publication]
        """

        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
            try:
                if query is None:
                    api_response = api_instance.get_publications(offset=offset, limit=limit)
                else:
                    api_response = api_instance.query_get_publications(query=query, offset=offset, limit=limit)
                return [Publication.from_dict(sub_data) for sub_data in api_response]
            except Exception as e:
                raise e

    def get_publication_by_id(self, id: str) -> Publication:
        """
        Retrieves a publication specified by its ID.

        Args:
            id (str): Unique identifier of a publication in database.

        Returns:
             Dataset: The publication corresponding to the given ID.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> asset_manager = AssetManager(...)
            >>> asset_manager.get_publication_by_id(id="pub_03F6jLXedDDQSzc6expGpLGI")
            Publication
        """

        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
            try:
                api_response = api_instance.get_publication_by_id(id)
                return Publication.from_dict(api_response)
            except Exception as e:
                raise e

    def get_platforms(self, offset: int = 0, limit: int = 100) -> List[Platform]:
        """
        Retrieves a list of platforms.

        Args:
            offset (int, optional): Starting index from which to retrieve. Defaults to 0.
            limit (int, optional): How many items to retrieve. Defaults to 100.

        Returns:
            List[Platform]: The list of platforms.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> asset_manager = AssetManager(...)
            >>> asset_manager.get_platforms(offset=2, limit=5)
            5
        """

        with ApiClient(self._config) as api_client:
            api_instance = AssetsApi(api_client)
            try:
                api_response = api_instance.get_platforms(offset=offset, limit=limit)
                return [Platform.from_dict(sub_data) for sub_data in api_response]
            except Exception as e:
                raise e
