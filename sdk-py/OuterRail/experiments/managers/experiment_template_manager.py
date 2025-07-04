from typing import Optional, List

from OuterRail import Configuration, ApiClient, ExperimentTemplatesApi, ExperimentTemplate


"""
    AIoD - RAIL

    ExperimentManager class

    Class aggregating methods for operating on multiple experiments.
"""


class ExperimentTemplateManager:
    def __init__(self, client_config: Configuration):
        """
        Initializes a new ExperimentTemplateManager.

        Args:
            client_config: (Configuration): Instance of Configuration class.

        Returns:
            ExperimentTemplateManager: Initialized  ExperimentTemplateManager.
        """
        self._config = client_config

    def count(self, query: str = "",
              mine: Optional[bool] = None,
              finalized: Optional[bool] = None,
              approved: Optional[bool] = None,
              public: Optional[bool] = None
              ) -> int:
        """
        Counts the number of experiments based on filters specified in Args.
        Args:
            query (str, optional): Query used to filter experiment templates. Defaults to empty string, which means that by default count is not filtered.
            mine (bool, optional): If own personal experiment templates should be counted or the opposite. Defaults to None.
            finalized (bool, optional): If experiment templates that are successfully build and ready to use should be counted or the opposite. Defaults to None.
            approved (bool, optional): If already approved experiments should be counted or the opposite. Defaults to None.
            public (bool, optional): If experiment templates flagged as public should be counted or the opposite. Defaults to None.

        Returns:
            int: Number of experiment templates.

        Raises:
            ApiException: In case of a failed HTTP request.
        """

        with ApiClient(self._config) as api_client:
            api_instance = ExperimentTemplatesApi(api_client)
            try:
                api_response = api_instance.get_experiment_templates_count_v1_count_experiment_templates_get(
                    query=query,
                    mine=mine,
                    approved=approved,
                    public=public,
                    finalized=finalized,
                )
                return api_response
            except Exception as e:
                raise e

    def get(self,
            query: str = "",
            mine: Optional[bool] = None,
            finalized: Optional[bool] = None,
            approved: Optional[bool] = None,
            public: Optional[bool] = None,
            offset: int = 0,
            limit: int = 100,
            ) -> List[ExperimentTemplate]:
        """
        Gets experiment templates based of on specified filters.

        Args:
            query (str, optional): Query used to filter experiment templates. Defaults to empty string, which means that by default, it's not used.
            mine (bool, optional): If own personal experiment templates should be included or the opposite. Defaults to None.
            finalized (bool, optional): If experiment templates that are successfully build and ready to use should be listed or the opposite. Defaults to None.
            approved (bool, optional): If already approved experiments should be listed or the opposite. Defaults to None.
            public (bool, optional): If experiment templates flagged as public should be listed or the opposite. Defaults to None.
            offset (int, optional): Starting index of experiment template range from which to retrieve Defaults to 0.
            limit (int, optional): Ending index of experiment template range to which to retrieve. Defaults to 100.

        Returns:
            list[ExperimentTemplateResponse]: List of all experiments in given range

        Raises:
            ApiException: In case of a failed HTTP request.
        """

        with ApiClient(self._config) as api_client:
            api_instance = ExperimentTemplatesApi(api_client)
            try:
                api_response = api_instance.get_experiment_templates_v1_experiment_templates_get(
                    query=query,
                    mine=mine,
                    approved=approved,
                    public=public,
                    finalized=finalized,
                    offset=offset,
                    limit=limit)
                return [ExperimentTemplate.from_dict(sub_data, self._config) for sub_data in api_response]
            except Exception as e:
                raise e

    def get_by_id(self, id: str) -> ExperimentTemplate:
        """
        Retrieves a specific experiment template by its ID.

        Args:
            id (str): ID of experiment template to be retrieved.

        Returns:
            ExperimentTemplate: Experiment template given by ID.

        Raises:
            ApiException: In case of a failed HTTP request.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentTemplatesApi(api_client)
            try:
                api_response = api_instance.get_experiment_template_v1_experiment_templates_id_get(id)
                return ExperimentTemplate.from_dict(api_response, self._config)
            except Exception as e:
                raise e

    def create(self, template: dict | tuple[str, str, str, dict]) -> ExperimentTemplate:
        """
        Creates a new experiment template.

        Args:
            template: (dict | tuple[str, str, str, dict]):
            The file can be passed either as full specified json (dictionary) or
            as a tuple of three strings with paths to: (script, requirements and docker imageand a json
            (dictionary) specifying the paths to script, requirements and docker image in this order and template
            description (name, description, task etc.).

        Returns:
            ExperimentTemplateResponse: Created experiment template.

        Raises:
            ApiException: In case of a failed HTTP request.
        """
        creation_dict = ExperimentTemplate.build_creation_dict(template)
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentTemplatesApi(api_client)
            try:
                api_response = api_instance.create_experiment_template_v1_experiment_templates_post(creation_dict)
                return ExperimentTemplate.from_dict(api_response, self._config)
            except Exception as e:
                raise e

