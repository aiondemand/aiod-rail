import json
from typing import Optional

from aiod_rail_sdk import (
    ApiClient,
    Configuration,
    ExperimentTemplateCreate,
    ExperimentTemplateResponse,
    ExperimentTemplatesApi,
)


class ExperimentTemplateClient:
    def __init__(self, client_config: Configuration):
        self._configuration = client_config

    def create_experiment_template(
        self, template: dict | tuple[str, str, str, dict]
    ) -> ExperimentTemplateResponse:
        """
        Creates experiment template for experiment.
        Args:
            template: (dict | tuple[str, str, str, dict]):  The file can be passed either as full specified json (dictionary)
                                                            or as a tuple of three strings and a json (dictionary) specifying
                                                            the paths to script, requirements and docker image in this order
                                                            and template description (name, description, task etc.).
        Returns:
            ExperimentTemplateResponse: Created experiment template.
        """
        experiment_template_instance = self._create_experiment_template_instance(
            template
        )

        with ApiClient(self._configuration) as api_client:
            api_instance = ExperimentTemplatesApi(api_client)
            experiment_template_create = experiment_template_instance

            try:
                api_response = api_instance.create_experiment_template_v1_experiment_templates_post(
                    experiment_template_create
                )
                return api_response

            except Exception as e:
                raise e

    def count(
        self,
        query: str = "",
        mine: Optional[bool] = None,
        finalized: Optional[bool] = None,
        approved: Optional[bool] = None,
        public: Optional[bool] = None,
    ) -> int:
        """
        Gets experiment templates count.
        Args:
            query (str, optional): Query used to filter experiment templates. Defaults to empty string, which means that by default count is not filtered.
            mine (bool, optional): If own personal experiment templates should be counted or the opposite. Defaults to None.
            finalized (bool, optional): If experiment templates that are successfully build and ready to use should be counted or the opposite. Defaults to None.
            approved (bool, optional): If already approved experiments should be counted or the opposite. Defaults to None.
            public (bool, optional): If experiment templates flagged as public should be counted or the opposite. Defaults to None.

        Returns:
            int: Number of experiment templates.
        """
        with ApiClient(self._configuration) as api_client:
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

    def get(
        self,
        query: str = "",
        mine: Optional[bool] = None,
        finalized: Optional[bool] = None,
        approved: Optional[bool] = None,
        public: Optional[bool] = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[ExperimentTemplateResponse]:
        """
        Gets experiment templates in specified range.
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
        """
        with ApiClient(self._configuration) as api_client:
            api_instance = ExperimentTemplatesApi(api_client)

            try:
                api_response = (
                    api_instance.get_experiment_templates_v1_experiment_templates_get(
                        query=query,
                        mine=mine,
                        approved=approved,
                        public=public,
                        finalized=finalized,
                        offset=offset,
                        limit=limit,
                    )
                )
                return api_response
            except Exception as e:
                raise e

    def get_by_id(self, id: str) -> ExperimentTemplateResponse:
        """
        Gets specific experiment template by its ID.
        Args:
            id (str): ID of experiment template to be retrieved.
        Returns:
            ExperimentTemplateResponse: Experiment template given by ID.
        """
        with ApiClient(self._configuration) as api_client:
            api_instance = ExperimentTemplatesApi(api_client)

            try:
                api_response = (
                    api_instance.get_experiment_template_v1_experiment_templates_id_get(
                        id
                    )
                )
                return api_response
            except Exception as e:
                raise e

    def remove(self, id: str) -> None:
        """
        Remove specific experiment template specified by ID.
        Args:
            id (str): ID of experiment template to be removed.
        Returns:
            None.
        """
        with ApiClient(self._configuration) as api_client:
            api_instance = ExperimentTemplatesApi(api_client)

            try:
                api_instance.remove_experiment_template_v1_experiment_templates_id_delete(
                    id=id
                )
            except Exception as e:
                raise e

    def archive(self, id: str, archive: bool = False) -> None:
        """
        Archives specific experiment template specified by ID.
        Args:
            id (str): ID of experiment template to be archived.
            archive (bool): If experiment template should be archived or un-archived. Defaults to False.
        Returns:
            None.
        """
        with ApiClient(self._configuration) as api_client:
            api_instance = ExperimentTemplatesApi(api_client)

            try:
                api_instance.archive_experiment_template_v1_experiment_templates_id_archive_patch(
                    id=id, archive=archive
                )
            except Exception as e:
                raise e

    def update(
        self, id: str, template: dict | tuple[str, str, str, dict]
    ) -> ExperimentTemplateResponse:
        """
        Updates specific experiment template.
        Args:
            id (str): ID of experiment template to be updated.
            template: (dict | tuple[str, str, str, dict]):  The file can be passed either as full specified json (dictionary)
                                                            or as a tuple of three strings and a json (dictionary) specifying
                                                            the paths to script, requirements and docker image in this order
                                                            and template description (name, description, task etc.).
        Returns:
            ExperimentTemplateResponse: Updated Experiment template by given ID.
        """
        experiment_template_instance = self._create_experiment_template_instance(
            template
        )

        with ApiClient(self._configuration) as api_client:
            api_instance = ExperimentTemplatesApi(api_client)

            try:
                api_response = api_instance.update_experiment_template_v1_experiment_templates_id_put(
                    id=id,
                    experiment_template_create=experiment_template_instance,
                )
                return api_response
            except Exception as e:
                raise e

    @staticmethod
    def _create_experiment_template_instance(
        template: dict | tuple[str, str, str, dict]
    ):
        if isinstance(template, dict):
            json_data = json.dumps(template)

        elif (
            isinstance(template, tuple)
            and len(template) == 4
            and all(isinstance(item, (str, dict)) for item in template)
        ):
            path_script, path_requirements, base_image, config = template
            if isinstance(config, dict):
                with (
                    open(path_script, "r") as s,
                    open(path_requirements, "r") as r,
                ):
                    script = s.read()
                    requirements = r.read()
                    config.update(
                        {
                            "script": script,
                            "pip_requirements": requirements,
                            "base_image": base_image,
                        }
                    )
                    json_data = json.dumps(config)
            else:
                raise ValueError("Fourth element must be a dictionary")
        else:
            raise ValueError("Invalid input format")

        return ExperimentTemplateCreate.from_json(json_data)
