import json
import aiod_rail_sdk
from typing import Union


class ExperimentsTemplates:
    def __init__(self, client_config: aiod_rail_sdk.Configuration):
        self._configuration = client_config
            
    def create_experiment_template(
            self, 
            authorization_header: dict,
            file: Union[dict, tuple[str, str, str, dict]]
            ) -> aiod_rail_sdk.ExperimentTemplateResponse:
        """
            Creates experiment template for experiment
            Args:
                authorization_header (dict): Authorization in form of token type and access token
                file: (Union[dict, tuple[str, str, str, dict]]): The file can be passed either as full specified json (dictionary)
                or as a tuple of three strings and a json (dictionary) specifying the paths to script, requirements and docker image
                in this order and template description (name, description, task etc.)
        """
        json_data = None
        if isinstance(file, dict):
            json_data = json.dumps(file)
        
        elif isinstance(file, tuple) and len(file) == 4 and all(isinstance(item, (str, dict)) for item in file):
            path_script, path_requirements, path_image, config = file
            if isinstance(config, dict):
                with open(path_script, 'r') as s, open(path_requirements, 'r') as r, open(path_image, 'r') as i:
                    script = s.read()
                    requirements = r.read()
                    image = i.read()
                    config.update({'script': script, 'pip_requirements': requirements, 'base_image': image})
                    json_data = json.dumps(config)
            else:
                raise ValueError("Fourth element must be a dictionary")
        else:
            raise ValueError("Invalid input format")
        
        experiment_template_create_instance = aiod_rail_sdk.ExperimentTemplateCreate.from_json(json_data)

        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
            api_client.default_headers = authorization_header
            api_instance = aiod_rail_sdk.ExperimentTemplatesApi(api_client)
            experiment_template_create = experiment_template_create_instance

            try:
                api_response = api_instance.create_experiment_template_v1_experiment_templates_post(experiment_template_create)
                return api_response
            
            except Exception as e:
                raise(f'Exception {e}')
            
            
    def approve_experiment_template(self, id: str, password: str = 'pass', is_approved: bool = False) -> None:
        """
            Approves experiment template with specified id
            Args:
                id (str): ID of experiment template to be approved
                password (str): Password required to be able to approve the experiment template
                approve_value (bool): Boolean value to approve/reject the experiment template
            Returns:
                object
        """
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
            api_instance = aiod_rail_sdk.ExperimentTemplatesApi(api_client)

            try:
                api_response = api_instance.approve_experiment_template_v1_experiment_templates_id_approve_patch(id, password, is_approved=is_approved)
                return api_response
            except Exception as e:
                raise(f'Exception {e}')

    def count(self, authorization_header: dict, include_mine: bool = True, include_approved: bool = False) -> int:
        """
            Gets experiment templates count
            Args:
                authorization_header (dict): Authorization in form of token type and access token
                include_mine (bool): If own personal experiment templates should be included in count (default False)
                include_approved (bool): If already approved experiments should be counted as well (default False)
        """
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
            api_client.default_headers = authorization_header
            api_instance = aiod_rail_sdk.ExperimentTemplatesApi(api_client)
            
            try:
                api_response = api_instance.get_experiment_templates_count_v1_count_experiment_templates_get(
                    include_mine=include_mine, include_approved=include_approved
                )
                return api_response
            except Exception as e:
                raise(f'Exception {e}')

    def get(self, authorization_header: dict, include_mine: bool = True, 
            include_approved: bool = True, offset: int = 0, limit: int = 100) -> list[aiod_rail_sdk.ExperimentTemplateResponse]:
        """
            Gets experiment templates
            Args:
                authorization_header (dict): Authorization in form of token type and access token
                include_mine (bool): If own personal experiment templates should be included (default True)
                include_approved (bool): If already approved experiments should be listed as well (default True)
                offset (int): Starting index of experiment template range from which to retrieve (default 0)
                limit (int): Ending index of experiment template range to which to retrieve (default 100)
        """
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
            api_client.default_headers = authorization_header
            api_instance = aiod_rail_sdk.ExperimentTemplatesApi(api_client)
            
            try:
                api_response = api_instance.get_experiment_templates_v1_experiment_templates_get(
                    include_mine=include_mine, include_approved=include_approved, offset=offset, limit=limit
                )
                return api_response
            except Exception as e:
                raise(f'Exception {e}')

    def get_by_id(self, id: str) -> aiod_rail_sdk.ExperimentTemplateResponse:
        """
            Gets specific experiment template by it's id
            Args:
                id (str): ID of experiment template to be retrieved
            Returns:
                ExperimentTemplateResponse: aiod_rail_sdk.models.experiment_template_response
        """
        with aiod_rail_sdk.ApiClient(self._configuration) as api_client:
            api_instance = aiod_rail_sdk.ExperimentTemplatesApi(api_client)
            
            try:
                api_response = api_instance.get_experiment_template_v1_experiment_templates_id_get(id)
                return api_response
            except Exception as e:
                raise(f'Exception {e}')
    