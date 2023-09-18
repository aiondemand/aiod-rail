# coding: utf-8

from __future__ import annotations

import re  # noqa: F401
from datetime import date, datetime  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401

from app.schemas.aiod_generated.aio_d_entry_create import AIoDEntryCreate
from app.schemas.aiod_generated.distribution import Distribution


class ServiceCreate(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    ServiceCreate - a model defined in OpenAPI

        platform: The platform of this ServiceCreate [Optional].
        platform_identifier: The platform_identifier of this ServiceCreate [Optional].
        name: The name of this ServiceCreate.
        description: The description of this ServiceCreate [Optional].
        same_as: The same_as of this ServiceCreate [Optional].
        slogan: The slogan of this ServiceCreate [Optional].
        terms_of_service: The terms_of_service of this ServiceCreate [Optional].
        aiod_entry: The aiod_entry of this ServiceCreate [Optional].
        alternate_name: The alternate_name of this ServiceCreate [Optional].
        application_area: The application_area of this ServiceCreate [Optional].
        contact: The contact of this ServiceCreate [Optional].
        has_part: The has_part of this ServiceCreate [Optional].
        industrial_sector: The industrial_sector of this ServiceCreate [Optional].
        is_part_of: The is_part_of of this ServiceCreate [Optional].
        keyword: The keyword of this ServiceCreate [Optional].
        media: The media of this ServiceCreate [Optional].
        note: The note of this ServiceCreate [Optional].
        research_area: The research_area of this ServiceCreate [Optional].
        scientific_domain: The scientific_domain of this ServiceCreate [Optional].
    """

    platform: Optional[str] = Field(alias="platform", default=None)
    platform_identifier: Optional[str] = Field(
        alias="platform_identifier", default=None
    )
    name: str = Field(alias="name")
    description: Optional[str] = Field(alias="description", default=None)
    same_as: Optional[str] = Field(alias="same_as", default=None)
    slogan: Optional[str] = Field(alias="slogan", default=None)
    terms_of_service: Optional[str] = Field(alias="terms_of_service", default=None)
    aiod_entry: Optional[AIoDEntryCreate] = Field(alias="aiod_entry", default=None)
    alternate_name: Optional[List[str]] = Field(alias="alternate_name", default=None)
    application_area: Optional[List[str]] = Field(
        alias="application_area", default=None
    )
    contact: Optional[List[int]] = Field(alias="contact", default=None)
    has_part: Optional[List[int]] = Field(alias="has_part", default=None)
    industrial_sector: Optional[List[str]] = Field(
        alias="industrial_sector", default=None
    )
    is_part_of: Optional[List[int]] = Field(alias="is_part_of", default=None)
    keyword: Optional[List[str]] = Field(alias="keyword", default=None)
    media: Optional[List[Distribution]] = Field(alias="media", default=None)
    note: Optional[List[str]] = Field(alias="note", default=None)
    research_area: Optional[List[str]] = Field(alias="research_area", default=None)
    scientific_domain: Optional[List[str]] = Field(
        alias="scientific_domain", default=None
    )

    @validator("platform")
    def platform_max_length(cls, value):
        assert len(value) <= 64
        return value

    @validator("platform_identifier")
    def platform_identifier_max_length(cls, value):
        assert len(value) <= 256
        return value

    @validator("name")
    def name_max_length(cls, value):
        assert len(value) <= 256
        return value

    @validator("description")
    def description_max_length(cls, value):
        assert len(value) <= 1800
        return value

    @validator("same_as")
    def same_as_max_length(cls, value):
        assert len(value) <= 256
        return value

    @validator("slogan")
    def slogan_max_length(cls, value):
        assert len(value) <= 256
        return value

    @validator("terms_of_service")
    def terms_of_service_max_length(cls, value):
        assert len(value) <= 1800
        return value


ServiceCreate.update_forward_refs()
