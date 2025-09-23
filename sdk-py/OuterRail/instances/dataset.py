import json
import pprint

from datetime import datetime
from typing_extensions import Annotated, Self
from typing import Any, ClassVar, Dict, List, Optional, Set
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr

from OuterRail import ApiClient, AssetsApi
from OuterRail import Note, AIoDEntryRead, DatasetSize, Distribution, Location, Text, Configuration


class Dataset(BaseModel):

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
    name: Annotated[str, Field(strict=True, max_length=256)]
    date_published: Optional[datetime] = Field(
        default=None,
        description="The datetime (utc) on which this resource was first published on an external platform. Note the difference between `.aiod_entry.date_created` and `.date_published`: the former is automatically set to the datetime the resource was created on AIoD, while the latter can optionally be set to an earlier datetime that the resource was published on an external platform.",
    )
    same_as: Optional[Annotated[str, Field(strict=True, max_length=256)]] = Field(
        default=None,
        description="Url of a reference Web page that unambiguously indicates this resource's identity.",
    )
    is_accessible_for_free: Optional[StrictBool] = Field(
        default=None,
        description="A flag to signal that this asset is accessible at no cost.",
    )
    version: Optional[Annotated[str, Field(strict=True, max_length=256)]] = Field(
        default=None, description="The version of this asset."
    )
    issn: Optional[
        Annotated[str, Field(min_length=8, strict=True, max_length=8)]
    ] = Field(
        default=None,
        description="The International Standard Serial Number, ISSN, an identifier for serial publications.",
    )
    measurement_technique: Optional[
        Annotated[str, Field(strict=True, max_length=256)]
    ] = Field(
        default=None,
        description="The technique, technology, or methodology used in a dataset, corresponding to the method used for measuring the corresponding variable(s).",
    )
    temporal_coverage: Optional[
        Annotated[str, Field(strict=True, max_length=64)]
    ] = Field(
        default=None,
        description="The temporalCoverage of a CreativeWork indicates the period that the content applies to, i.e. that it describes, a textual string indicating a time period in ISO 8601 time interval format. In the case of a Dataset it will typically indicate the relevant time period in a precise notation (e.g. for a 2011 census dataset, the year 2011 would be written '2011/2012').",
    )
    ai_asset_identifier: Optional[StrictStr] = None
    ai_resource_identifier: Optional[StrictStr] = Field(
        default=None,
        description="This resource can be identified by its own identifier, but also by the resource_identifier.",
    )
    aiod_entry: Optional[AIoDEntryRead] = None
    alternate_name: Optional[List[StrictStr]] = Field(
        default=None,
        description="An alias for the item, commonly used for the resource instead of the name.",
    )
    application_area: Optional[List[StrictStr]] = Field(
        default=None, description="The objective of this AI resource."
    )
    citation: Optional[List[StrictInt]] = Field(
        default=None, description="A bibliographic reference."
    )
    contact: Optional[List[StrictInt]] = Field(
        default=None,
        description="Contact information of persons/organisations that can be contacted about this resource.",
    )
    creator: Optional[List[StrictInt]] = Field(
        default=None,
        description="Contact information of persons/organisations that created this resource.",
    )
    description: Optional[Text] = None
    distribution: Optional[List[Distribution]] = None
    funder: Optional[List[StrictInt]] = Field(
        default=None,
        description="Links to identifiers of the agents (person or organization) that supports this dataset through some kind of financial contribution. ",
    )
    has_part: Optional[List[StrictInt]] = None
    industrial_sector: Optional[List[StrictStr]] = Field(
        default=None,
        description="A business domain where a resource is or can be used.",
    )
    is_part_of: Optional[List[StrictInt]] = None
    keyword: Optional[List[StrictStr]] = Field(
        default=None,
        description="Keywords or tags used to describe this resource, providing additional context.",
    )
    license: Optional[StrictStr] = None
    media: Optional[List[Distribution]] = Field(
        default=None,
        description="Images or videos depicting the resource or associated with it. ",
    )
    note: Optional[List[Note]] = Field(
        default=None, description="Notes on this AI resource."
    )
    relevant_link: Optional[List[StrictStr]] = Field(
        default=None,
        description="URLs of relevant resources. These resources should not be part of AIoD (use relevant_resource otherwise). This field should only be used if there is no more specific field.",
    )
    relevant_resource: Optional[List[StrictInt]] = None
    relevant_to: Optional[List[StrictInt]] = None
    research_area: Optional[List[StrictStr]] = Field(
        default=None,
        description="The research area is similar to the scientific_domain, but more high-level.",
    )
    scientific_domain: Optional[List[StrictStr]] = Field(
        default=None,
        description="The scientific domain is related to the methods with which an objective is reached.",
    )
    size: Optional[DatasetSize] = Field(
        default=None,
        description="The size of this dataset, for example the number of rows. The file size should not be included here, but in distribution.content_size_kb.",
    )
    spatial_coverage: Optional[Location] = Field(
        default=None,
        description="A location that describes the spatial aspect of this dataset. For example, a point where all the measurements were collected.",
    )
    identifier: StrictStr
    __properties: ClassVar[List[str]] = [
        "platform",
        "platform_resource_identifier",
        "name",
        "date_published",
        "same_as",
        "is_accessible_for_free",
        "version",
        "issn",
        "measurement_technique",
        "temporal_coverage",
        "ai_asset_identifier",
        "ai_resource_identifier",
        "aiod_entry",
        "alternate_name",
        "application_area",
        "citation",
        "contact",
        "creator",
        "description",
        "distribution",
        "funder",
        "has_part",
        "industrial_sector",
        "is_part_of",
        "keyword",
        "license",
        "media",
        "note",
        "relevant_link",
        "relevant_resource",
        "relevant_to",
        "research_area",
        "scientific_domain",
        "size",
        "spatial_coverage",
        "identifier",
    ]

    model_config = ConfigDict(populate_by_name=True, validate_assignment=True, protected_namespaces=())

    def _set_config(self, config: Configuration) -> None:
        """
        Sets the configuration for API calls.

        Args:
        config (Configuration): The api configuration.

        Returns:
            None:
        """

        self._config = config

    def delete(self) -> None:
        """
        Deletes specific dataset. Afterward, operations on deleted instance will result in HTTP exception.

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
            api_instance = AssetsApi(api_client)
            try:
                api_instance.delete_dataset(id=self.identifier)
                self._deleted = True
            except Exception as e:
                raise e

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of Dataset from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of aiod_entry
        if self.aiod_entry:
            _dict["aiod_entry"] = self.aiod_entry.to_dict()
        # override the default output from pydantic by calling `to_dict()` of description
        if self.description:
            _dict["description"] = self.description.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in distribution (list)
        _items = []
        if self.distribution:
            for _item in self.distribution:
                if _item:
                    _items.append(_item.to_dict())
            _dict["distribution"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in media (list)
        _items = []
        if self.media:
            for _item in self.media:
                if _item:
                    _items.append(_item.to_dict())
            _dict["media"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in note (list)
        _items = []
        if self.note:
            for _item in self.note:
                if _item:
                    _items.append(_item.to_dict())
            _dict["note"] = _items
        # override the default output from pydantic by calling `to_dict()` of size
        if self.size:
            _dict["size"] = self.size.to_dict()
        # override the default output from pydantic by calling `to_dict()` of spatial_coverage
        if self.spatial_coverage:
            _dict["spatial_coverage"] = self.spatial_coverage.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]], config: Configuration = None) -> Optional[Self]:
        """Create an instance of Dataset from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            _obj = cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "platform": obj.get("platform"),
                "platform_resource_identifier": obj.get("platform_resource_identifier"),
                "name": obj.get("name"),
                "date_published": obj.get("date_published"),
                "same_as": obj.get("same_as"),
                "is_accessible_for_free": obj.get("is_accessible_for_free"),
                "version": obj.get("version"),
                "issn": obj.get("issn"),
                "measurement_technique": obj.get("measurement_technique"),
                "temporal_coverage": obj.get("temporal_coverage"),
                "ai_asset_identifier": obj.get("ai_asset_identifier"),
                "ai_resource_identifier": obj.get("ai_resource_identifier"),
                "aiod_entry": (
                    AIoDEntryRead.from_dict(obj["aiod_entry"])
                    if obj.get("aiod_entry") is not None
                    else None
                ),
                "alternate_name": obj.get("alternate_name"),
                "application_area": obj.get("application_area"),
                "citation": obj.get("citation"),
                "contact": obj.get("contact"),
                "creator": obj.get("creator"),
                "description": (
                    Text.from_dict(obj["description"])
                    if obj.get("description") is not None
                    else None
                ),
                "distribution": (
                    [Distribution.from_dict(_item) for _item in obj["distribution"]]
                    if obj.get("distribution") is not None
                    else None
                ),
                "funder": obj.get("funder"),
                "has_part": obj.get("has_part"),
                "industrial_sector": obj.get("industrial_sector"),
                "is_part_of": obj.get("is_part_of"),
                "keyword": obj.get("keyword"),
                "license": obj.get("license"),
                "media": (
                    [Distribution.from_dict(_item) for _item in obj["media"]]
                    if obj.get("media") is not None
                    else None
                ),
                "note": (
                    [Note.from_dict(_item) for _item in obj["note"]]
                    if obj.get("note") is not None
                    else None
                ),
                "relevant_link": obj.get("relevant_link"),
                "relevant_resource": obj.get("relevant_resource"),
                "relevant_to": obj.get("relevant_to"),
                "research_area": obj.get("research_area"),
                "scientific_domain": obj.get("scientific_domain"),
                "size": (
                    DatasetSize.from_dict(obj["size"])
                    if obj.get("size") is not None
                    else None
                ),
                "spatial_coverage": (
                    Location.from_dict(obj["spatial_coverage"])
                    if obj.get("spatial_coverage") is not None
                    else None
                ),
                "identifier": obj.get("identifier"),
            }
        )
        if config is not None:
            _obj._set_config(config)
        return _obj
