import json
import aiod_rail_sdk


class Experiments:
    # TODO change to client.py strategy
    def __init__(self, client_config):
        self._configuration = client_config
        
    def create_experiment(self) -> aiod_rail_sdk.ExperimentResponse:
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
            api_instance = aiod_rail_sdk.ExperimentsApi(api_client)
            experiment_create = aiod_rail_sdk.ExperimentCreate()

            try:
                api_response = api_instance.create_experiment_v1_experiments_post(experiment_create)
                return api_response
            
            except Exception as e:
                raise(f'Exception {e}')
            
    

    