import json
import pprint

from typing_extensions import Annotated, Self
from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional, Set



class Address(BaseModel):

    region: Optional[Annotated[str, Field(strict=True, max_length=256)]] = Field(
        default=None,
        description="A subdivision of the country. Not necessary for most countries. ",
    )
    locality: Optional[Annotated[str, Field(strict=True, max_length=256)]] = Field(
        default=None, description="A city, town or village."
    )
    street: Optional[Annotated[str, Field(strict=True, max_length=256)]] = Field(
        default=None, description="The street address."
    )
    postal_code: Optional[Annotated[str, Field(strict=True, max_length=64)]] = Field(
        default=None, description="The postal code."
    )
    address: Optional[Annotated[str, Field(strict=True, max_length=256)]] = Field(
        default=None,
        description="Free text, in case the separate parts such as the street, postal code and country cannot be confidently separated.",
    )
    country: Optional[
        Annotated[str, Field(min_length=3, strict=True, max_length=3)]
    ] = Field(default=None, description="The country as ISO 3166-1 alpha-3")
    __properties: ClassVar[List[str]] = [
        "region",
        "locality",
        "street",
        "postal_code",
        "address",
        "country",
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
        """Create an instance of Address from a JSON string"""
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
        """Create an instance of Address from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "region": obj.get("region"),
                "locality": obj.get("locality"),
                "street": obj.get("street"),
                "postal_code": obj.get("postal_code"),
                "address": obj.get("address"),
                "country": obj.get("country"),
            }
        )
        return _obj
