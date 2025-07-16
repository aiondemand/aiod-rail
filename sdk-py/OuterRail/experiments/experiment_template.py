import json

from typing_extensions import Self
from typing import Any, ClassVar, Dict, List, Optional
from pydantic import BaseModel, StrictBool, StrictStr, ConfigDict

from OuterRail import Configuration, ApiClient, ExperimentTemplatesApi
from OuterRail.models.task_type import TaskType
from OuterRail.models.asset_schema import AssetSchema
from OuterRail.models.environment_var_def import EnvironmentVarDef




class ExperimentTemplate(BaseModel):
    """
        AIoD - RAIL

        ExperimentTemplate class.

        Implementation of class representing an instance of experiment template and methods
        operating with this instance.
    """

    id: StrictStr
    name: StrictStr
    state: StrictStr
    script: StrictStr
    created_at: StrictStr
    updated_at: StrictStr
    dockerfile: StrictStr
    base_image: StrictStr
    description: StrictStr
    pip_requirements: StrictStr
    is_mine: StrictBool
    is_public: StrictBool
    is_archived: StrictBool
    is_approved: Optional[StrictBool]
    task: TaskType
    datasets_schema: AssetSchema
    models_schema: AssetSchema
    envs_required: List[EnvironmentVarDef]
    envs_optional: List[EnvironmentVarDef]
    __properties: ClassVar[List[str]] = [
        "name", "description", "task", "datasets_schema", "models_schema", "envs_required", "envs_optional",
        "script", "pip_requirements", "is_public", "id", "created_at", "updated_at", "state", "dockerfile",
        "is_archived", "is_approved", "is_mine", "base_image"
    ]
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True, protected_namespaces=())

    def archive(self, archive: bool = False) -> None:
        """
        Archives specific experiment template specified by ID.

        Args:
            archive (bool): If experiment template should be archived or un-archived. Defaults to False.
        Returns:
            None.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> self.archive(True)
            >>> self.is_archived
            True

        """

        with ApiClient(self._config) as api_client:
            api_instance = ExperimentTemplatesApi(api_client)
            try:
                api_instance.archive_experiment_template_v1_experiment_templates_id_archive_patch(
                    id=self.id, archive=archive
                )
                self.is_archived = archive
            except Exception as e:
                raise e

    def update(self, template: dict | tuple[str, str, str, dict]) -> Self:
        """
        Updates specific experiment template.

        Args:
            template: (dict | tuple[str, str, str, dict]):  The file can be passed either as full specified json (dictionary)
                                                            or as a tuple of three strings and a json (dictionary) specifying
                                                            the paths to script, requirements and docker image in this order
                                                            and template description (name, description, task etc.).

        Returns:
            ExperimentTemplateResponse: Updated Experiment template by given ID.

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
            >>> self.update((script_path, requirements_path, base_image, template_config))
            Self # The instance is also updated in place.
        """

        update_dict = self.build_creation_dict(template)
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentTemplatesApi(api_client)
            try:
                api_response = api_instance.update_experiment_template_v1_experiment_templates_id_put(
                    id=self.id,
                    experiment_template_create=update_dict,
                )
                self.__dict__.update(api_response)
                return self
            except Exception as e:
                raise e

    def delete(self) -> None:
        """
        Deletes the experiment template. After this method is called any operations on the template instance will
        result in an HTTP exception as the template no longer exists.

        Returns:
            None.

        Raises:
            ApiException: In case of a failed HTTP request.

        Examples:
            >>> self.delete()
            >>> self._deleted
            True
        """

        with ApiClient(self._config) as api_client:
            api_instance = ExperimentTemplatesApi(api_client)
            try:
                api_instance.remove_experiment_template_v1_experiment_templates_id_delete(id=self.id)
                self._deleted = True
            except Exception as e:
                raise e

    def _set_config(self, config: Configuration) -> None:
        """
        Sets the configuration of the experiment template required for API calls.

        Args:
        config (Configuration): The api configuration.

        Returns:
            None:
        """

        self._config = config

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """
        Creates an instance of ExperimentTemplate from a JSON string.

        Args:
            json_str: The JSON string to create the instance from.

        Returns:
            ExperimentTemplate: Instance of ExperimentTemplate.

        Examples:
            >>> template_json = ...
            >>> ExperimentTemplate.from_json(template_json)
            ExperimentTemplate
        """

        return cls.from_dict(json.loads(json_str))

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]], config: Configuration = None) -> Optional[Self]:
        """
        Creates an instance of ExperimentTemplate from a dict.

        Args:
            obj (Optional[Dict[str, Any]]): Dictionary representation of an ExperimentTemplate
            config (Configuration): Configuration associated with API calls.

        Returns:
            ExperimentTemplate: An instance of ExperimentTemplate.

        Examples:
            >>> template_dict = ...
            >>> ExperimentTemplate.from_dict(template_dict)
            ExperimentTemplate
        """

        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        obj["base_image"] = obj.get("base_image", "FIX ME")
        tmp = {
            "datasets_schema": (
                AssetSchema.from_dict(obj.pop("datasets_schema"))
                if obj.get("datasets_schema") is not None
                else None
            ),
            "models_schema": (
                AssetSchema.from_dict(obj.pop("models_schema"))
                if obj.get("models_schema") is not None
                else None
            ),
            "envs_required": (
                [
                    EnvironmentVarDef.from_dict(_item)
                    for _item in obj.pop("envs_required")
                ]
                if obj.get("envs_required") is not None
                else None
            ),
            "envs_optional": (
                [
                    EnvironmentVarDef.from_dict(_item)
                    for _item in obj.pop("envs_optional")
                ]
                if obj.get("envs_optional") is not None
                else None
            ),
        }
        tmp.update(obj)
        _obj = cls.model_validate(tmp)
        if config is not None:
            _obj._set_config(config)
        return _obj

    @staticmethod
    def build_creation_dict( template: dict | tuple[str, str, str, dict]):
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

        return json.loads(json_data)
