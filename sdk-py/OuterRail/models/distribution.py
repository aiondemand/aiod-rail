import json
import pprint

from typing_extensions import Annotated, Self
from typing import Any, ClassVar, Dict, List, Optional, Set
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr


class Distribution(BaseModel):

    platform: Optional[Annotated[str, Field(strict=True, max_length=64)]] = Field(
        default=None,
        description="The external platform from which this resource originates. Leave empty if this item originates from AIoD. If platform is not None, the platform_resource_identifier should be set as well.",
    )
    platform_resource_identifier: Optional[
        Annotated[str, Field(strict=True, max_length=256)]
    ] = Field(
        default=None,
        description="A unique identifier issued by the external platform that's specified in 'platform'. Leave empty if this item is not part of an external platform. For example, for HuggingFace, this should be the <namespace>/<dataset_name>, and for Openml, the OpenML identifier.",
    )
    checksum: Optional[Annotated[str, Field(strict=True, max_length=1800)]] = Field(
        default=None,
        description="The value of a checksum algorithm ran on this content.",
    )
    checksum_algorithm: Optional[
        Annotated[str, Field(strict=True, max_length=64)]
    ] = Field(default=None, description="The checksum algorithm.")
    copyright: Optional[Annotated[str, Field(strict=True, max_length=256)]] = None
    content_url: Optional[Annotated[str, Field(strict=True, max_length=1800)]] = None
    content_size_kb: Optional[StrictInt] = None
    date_published: Optional[StrictStr] = Field(
        default=None,
        description="The datetime (utc) on which this Distribution was first published on an external platform. ",
    )
    description: Optional[Annotated[str, Field(strict=True, max_length=1800)]] = None
    encoding_format: Optional[
        Annotated[str, Field(strict=True, max_length=256)]
    ] = Field(default=None, description="The mimetype of this file.")
    name: Optional[Annotated[str, Field(strict=True, max_length=256)]] = None
    technology_readiness_level: Optional[StrictInt] = Field(
        default=None,
        description="The technology readiness level (TRL) of the distribution. TRL 1 is the lowest and stands for 'Basic principles observed', TRL 9 is the highest and stands for 'actual system proven in operational environment'.",
    )
    binary_blob: Optional[bytes] = Field(
        default=None,
        description="Binary blob for storing image (or other type of media) data. You may not set this property directly, set it indirectly through dedicated endpoints such as /organisations/{identifier}/image instead.",
    )
    __properties: ClassVar[List[str]] = [
        "platform",
        "platform_resource_identifier",
        "checksum",
        "checksum_algorithm",
        "copyright",
        "content_url",
        "content_size_kb",
        "date_published",
        "description",
        "encoding_format",
        "name",
        "technology_readiness_level",
        "binary_blob",
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
        """Create an instance of Distribution from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Distribution from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "platform": obj.get("platform"),
                "platform_resource_identifier": obj.get("platform_resource_identifier"),
                "checksum": obj.get("checksum"),
                "checksum_algorithm": obj.get("checksum_algorithm"),
                "copyright": obj.get("copyright"),
                "content_url": obj.get("content_url"),
                "content_size_kb": obj.get("content_size_kb"),
                "date_published": obj.get("date_published"),
                "description": obj.get("description"),
                "encoding_format": obj.get("encoding_format"),
                "name": obj.get("name"),
                "technology_readiness_level": obj.get("technology_readiness_level"),
            }
        )
        return _obj
