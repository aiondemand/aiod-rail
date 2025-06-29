from __future__ import annotations

import json
from typing_extensions import Self
from typing import Any, ClassVar, Dict, List, Optional
from pydantic import BaseModel, StrictBool, StrictStr

from OuterRail import Configuration, ApiClient, ExperimentTemplatesApi
from OuterRail.models.task_type import TaskType
from OuterRail.models.asset_schema import AssetSchema
from OuterRail.models.environment_var_def import EnvironmentVarDef

"""
    AIoD - RAIL

    ExperimentTemplate class. 
    
    Implementation of class representing an instance of experiment template and methods
    operating with this instance.
"""


class ExperimentTemplate(BaseModel):
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
        "id", "name", "description", "task", "datasets_schema", "models_schema", "envs_required", "envs_optional",
        "script", "pip_requirements", "is_public", "is_archived", "base_image"
    ]

    def archive(self, archive: bool = False) -> None:
        """
        Archives specific experiment template specified by ID.

        Args:
            archive (bool): If experiment template should be archived or un-archived. Defaults to False.
        Returns:
            None.

        Raises:
            ApiException: In case of a failed HTTP request.
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

    def update(self, template: dict | tuple[str, str, str, dict]) -> ExperimentTemplate:
        """
        Updates specific experiment template.
        Args:
            template: (dict | tuple[str, str, str, dict]):  The file can be passed either as full specified json (dictionary)
                                                            or as a tuple of three strings and a json (dictionary) specifying
                                                            the paths to script, requirements and docker image in this order
                                                            and template description (name, description, task etc.).
        Returns:
            ExperimentTemplateResponse: Updated Experiment template by given ID.
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

    def remove(self) -> None:
        """
        Removes the experiment template. This method also invalidates the self instance of experiment template.

        Returns:
            None.

        Raises:
            ApiException: In case of a failed HTTP request.
        """
        with ApiClient(self._config) as api_client:
            api_instance = ExperimentTemplatesApi(api_client)
            try:
                api_instance.remove_experiment_template_v1_experiment_templates_id_delete(id=self.id)
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
        Creates an instance of ExperimentTemplateCreate from a JSON string.

        Args:
            json_str: The JSON string to create the instance from.

        Returns:
            ExperimentTemplate: Instance of ExperimentTemplate.
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


# class ExperimentTemplateCreate(BaseModel):
#     """
#     ExperimentTemplateCreate
#     """  # noqa: E501
#
#     name: StrictStr
#     description: StrictStr
#     task: TaskType
#     datasets_schema: AssetSchema
#     models_schema: AssetSchema
#     envs_required: List[EnvironmentVarDef]
#     envs_optional: List[EnvironmentVarDef]
#     script: StrictStr
#     pip_requirements: StrictStr
#     is_public: StrictBool
#     base_image: StrictStr
#     __properties: ClassVar[List[str]] = [
#         "name",
#         "description",
#         "task",
#         "datasets_schema",
#         "models_schema",
#         "envs_required",
#         "envs_optional",
#         "script",
#         "pip_requirements",
#         "is_public",
#         "base_image",
#     ]
#
#     model_config = ConfigDict(
#         populate_by_name=True,
#         validate_assignment=True,
#         protected_namespaces=(),
#     )
#
#     def to_str(self) -> str:
#         """Returns the string representation of the model using alias"""
#         return pprint.pformat(self.model_dump(by_alias=True))
#
#     def to_json(self) -> str:
#         """Returns the JSON representation of the model using alias"""
#         # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
#         return json.dumps(self.to_dict())
#
#     @classmethod
#     def from_json(cls, json_str: str) -> Optional[Self]:
#         """Create an instance of ExperimentTemplateCreate from a JSON string"""
#         return cls.from_dict(json.loads(json_str))
#
#     def to_dict(self) -> Dict[str, Any]:
#         """Return the dictionary representation of the model using alias.
#
#         This has the following differences from calling pydantic's
#         `self.model_dump(by_alias=True)`:
#
#         * `None` is only added to the output dict for nullable fields that
#           were set at model initialization. Other fields with value `None`
#           are ignored.
#         """
#         excluded_fields: Set[str] = set([])
#
#         _dict = self.model_dump(
#             by_alias=True,
#             exclude=excluded_fields,
#             exclude_none=True,
#         )
#         # override the default output from pydantic by calling `to_dict()` of datasets_schema
#         if self.datasets_schema:
#             _dict["datasets_schema"] = self.datasets_schema.to_dict()
#         # override the default output from pydantic by calling `to_dict()` of models_schema
#         if self.models_schema:
#             _dict["models_schema"] = self.models_schema.to_dict()
#         # override the default output from pydantic by calling `to_dict()` of each item in envs_required (list)
#         _items = []
#         if self.envs_required:
#             for _item in self.envs_required:
#                 if _item:
#                     _items.append(_item.to_dict())
#             _dict["envs_required"] = _items
#         # override the default output from pydantic by calling `to_dict()` of each item in envs_optional (list)
#         _items = []
#         if self.envs_optional:
#             for _item in self.envs_optional:
#                 if _item:
#                     _items.append(_item.to_dict())
#             _dict["envs_optional"] = _items
#         return _dict
