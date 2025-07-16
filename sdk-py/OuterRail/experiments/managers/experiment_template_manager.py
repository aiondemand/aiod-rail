from typing import Optional, List

from OuterRail import Configuration, ApiClient, ExperimentTemplatesApi, ExperimentTemplate


class ExperimentTemplateManager:

    """
        AIoD - RAIL

        ExperimentManager class

        Class aggregating methods for operating on multiple experiments.
    """

    def __init__(self, client_config: Configuration):
        """
        Initializes a new ExperimentTemplateManager.

        Args:
            client_config: (Configuration): Instance of Configuration class.

        Returns:
            ExperimentTemplateManager: Initialized  ExperimentTemplateManager.

        Examples:
            >>> config = Configuration(...)
            >>> ExperimentTemplateManager(config)
            ExperimentTemplateManager
        """
        self._config = client_config

    def count(self,
              query: str = "",
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

        Examples:
            >>> template_manager = ExperimentTemplateManager(...)
            >>> template_manager.count(finalized=True, approved=True, public=True)
            1234
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
            query (str, optional): Query used to filter experiment templates.
                This parameter is case-insensitive and matches full words in template names.
                Defaults to empty string, in which case it's not used.
            mine (bool, optional): If own personal experiment templates should be included or the opposite. Defaults to None.
            finalized (bool, optional): If experiment templates that are successfully build and ready to use should be listed or the opposite. Defaults to None.
            approved (bool, optional): If already approved experiments should be listed or the opposite. Defaults to None.
            public (bool, optional): If experiment templates flagged as public should be listed or the opposite. Defaults to None.
            offset (int, optional): Starting index of experiment template range from which to retrieve Defaults to 0.
            limit (int, optional): Ending index of experiment template range to which to retrieve. Defaults to 100.

        Returns:
            list[ExperimentTemplate]: List of all experiments in given range

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> template_manager = ExperimentTemplateManager(...)
            >>> template_manager.get()
            List[ExperimentTemplate]
            >>> len(template_manager.get(finalized=True, approved=True, limit=1000))
            1000
            >>> template_manager.get(query="Tutorial")
            List[ExperimentTemplate] # only templates that contain word "Tutorial" in their name.
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

        Examples:
            >>> template_manager = ExperimentTemplateManager(...)
            >>> template_manager.get_by_id("685151f2d08da970a3a5d6ce")
            ExperimentTemplate
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
            as a tuple of three strings with paths to: (script, requirements and docker image and a json
            (dictionary) specifying the paths to script, requirements and docker image in this order and template
            description (name, description, task etc.).

        Returns:
            ExperimentTemplate: Created experiment template.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> script_path = "path/to/script.py"
            >>> requirements_path = "path/to/requirements.txt"
            >>> base_image = "python:3.9"
            >>> template_config = {
            >>> "name": "Example Template",
            >>> "description": "Template in Examples",
            >>> "task": "TEXT_CLASSIFICATION",
            >>> "datasets_schema": { "cardinality": "1-1" },
            >>> "models_schema": { "cardinality": "1-1" },
            >>> "envs_required": [ { "name": "SPLIT_NAME", "description": "name of a subset" } ],
            >>> "envs_optional": [],
            >>> "available_metrics": [ "accuracy" ],
            >>> "is_public": True
            >>> }
            >>> template_manager.create((script_path, requirements_path, base_image, template_config))
            ExperimentTemplate # newly created instance
        """
        creation_dict = ExperimentTemplate.build_creation_dict(template)
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentTemplatesApi(api_client)
            try:
                api_response = api_instance.create_experiment_template_v1_experiment_templates_post(creation_dict)
                return ExperimentTemplate.from_dict(api_response, self._config)
            except Exception as e:
                raise e

