import json
import aiod_rail_sdk


class Experiments:
    def __init__(self, client_config: aiod_rail_sdk.Configuration):
        self._configuration = client_config
        
    def create_experiment(self, authorization_header: dict, file) -> aiod_rail_sdk.ExperimentResponse:
        """
            Creates experiment from specified experiment template.
            Args:
                authorization_header (dict): Authorization in form of token type and access token.
                file (dict): Experiment template described in json file.

            Returns:
                aiod_rail_sdk.ExperimentResponse: Experiment created from given template.
        """
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
            json_data = json.dumps(file)
            experiment_create_instance = aiod_rail_sdk.ExperimentCreate.from_json(json_data)
            api_client.default_headers = authorization_header
            try:
                api_response = api_instance.create_experiment_v1_experiments_post(experiment_create_instance)
                return api_response
            
            except Exception as e:
                raise(f'Exception {e}')
            
    
    def run_experiment(self, authorization_header: dict, id: str) -> aiod_rail_sdk.ExperimentRunResponse:
        """
            Runs specified experiment.
            Args:
                authorization_header (dict): Authorization in form of token type and access token.
                id (str): ID of experiment to be run.
            #TODO
            Returns:

        """
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
            api_client.default_headers = authorization_header
            try:
                api_response = api_instance.execute_experiment_run_v1_experiments_id_execute_get(id)
                return api_response
            
            except Exception as e:
                raise(f'Exception {e}')



    def logs(self, authorization_header: dict, id: str) -> str:
        """
            Get experiment run logs.
            Args:
                authorization_header (dict): Authorization in form of token type and access token.
                id (str): ID of experiment run from which logs are to be retrieved.
            
            Returns:
                str: Logs of experiment run given by ID.
        """
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
            api_client.default_headers = authorization_header
            try:
                api_response = api_instance.get_experiment_run_logs_v1_experiment_runs_id_logs_get(id)
                return api_response
            except Exception as e:
                print(f'Exception {e}')

    def count(self, authorization_header: dict) -> int:
        """
            Gets experiment count.
            Args:
                authorization_header (dict): Authorization in form of token type and access token.
            
            Returns:
                int: Number of experiments.
        """
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
            api_client.default_headers = authorization_header
            try:
                api_response = api_instance.get_experiments_count_v1_count_experiments_get()
                return api_response
            except Exception as e:
                print(f'Exception {e}')

    def get(self, authorization_header: dict, offset: int = 0, limit: int = 100) -> list[aiod_rail_sdk.ExperimentResponse]:
        """
            Gets experiments in specified range.
            Args:
                authorization_header (dict): Authorization in form of token type and access token.
                offset (int, optional): Starting index of experiment range from which to retrieve (default 0).
                limit (int, optional): Ending index of experiment range to which to retrieve (default 100).
            
            Returns:
                list[aiod_rail_sdk.ExperimentResponse]: The list of experiments.
        """
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
            api_client.default_headers = authorization_header
            try:
                api_response = api_instance.get_experiments_v1_experiments_get(offset, limit)
                return api_response
            except Exception as e:
                print(f'Exception {e}')


    def get_by_id(self, authorization_header: dict, id: str) -> aiod_rail_sdk.ExperimentResponse:
        """
            Gets specific experiment by it's ID.
            Args:
                authorization_header (dict): Authorization in form of token type and access token.
                id (str): ID of experiment to be retrieved.
            
            Returns:
                aiod_rail_sdk.ExperimentResponse: Experiment specified by given ID.
        """
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
            api_client.default_headers = authorization_header
            try:
                api_response = api_instance.get_experiment_v1_experiments_id_get(id)
                return api_response
            except Exception as e:
                print(f'Exception {e}')


    def download(self, authorization_header: dict, id: str, filepath: str) -> None:
        """
            Downloads experiment specified by ID to specified filepath.
            Args:
                authorization_header (dict): Authorization in form of token type and access token.
                id (str): ID of experiment to be downloaded.
                filepath (str): Path to which file will be stored.
            
            Returns:
                None.
        """
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
            api_client.default_headers = authorization_header
            try:
                api_response = api_instance.download_file_v1_experiment_runs_id_files_download_get(id, filepath)
            except Exception as e:
                print(f'Exception {e}')

    
        