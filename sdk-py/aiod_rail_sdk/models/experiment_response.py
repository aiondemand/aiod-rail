# coding: utf-8

"""
    AIoD - RAIL

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.0.20240603-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional, Set

from aiod_rail_sdk.models.environment_var import EnvironmentVar
from pydantic import BaseModel, ConfigDict, StrictBool, StrictStr
from typing_extensions import Self


class ExperimentResponse(BaseModel):
    """
    ExperimentResponse
    """  # noqa: E501

    name: StrictStr
    description: StrictStr
    is_public: StrictBool
    experiment_template_id: StrictStr
    dataset_ids: List[StrictStr]
    model_ids: List[StrictStr]
    publication_ids: Optional[List[StrictStr]] = None
    env_vars: List[EnvironmentVar]
    id: StrictStr
    created_at: datetime
    updated_at: datetime
    is_archived: StrictBool
    is_mine: StrictBool
    __properties: ClassVar[List[str]] = [
        "name",
        "description",
        "is_public",
        "experiment_template_id",
        "dataset_ids",
        "model_ids",
        "publication_ids",
        "env_vars",
        "id",
        "created_at",
        "updated_at",
        "is_archived",
        "is_mine",
    ]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of ExperimentResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in env_vars (list)
        _items = []
        if self.env_vars:
            for _item in self.env_vars:
                if _item:
                    _items.append(_item.to_dict())
            _dict["env_vars"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ExperimentResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "name": obj.get("name"),
                "description": obj.get("description"),
                "is_public": obj.get("is_public"),
                "experiment_template_id": obj.get("experiment_template_id"),
                "dataset_ids": obj.get("dataset_ids"),
                "model_ids": obj.get("model_ids"),
                "publication_ids": obj.get("publication_ids"),
                "env_vars": (
                    [EnvironmentVar.from_dict(_item) for _item in obj["env_vars"]]
                    if obj.get("env_vars") is not None
                    else None
                ),
                "id": obj.get("id"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "is_archived": obj.get("is_archived"),
                "is_mine": obj.get("is_mine"),
            }
        )
        return _obj
