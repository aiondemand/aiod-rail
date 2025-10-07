from typing_extensions import Annotated
from typing import List, Optional
from pydantic import BaseModel, Field, StrictStr

from OuterRail.models.aio_d_entry_read import AIoDEntryRead
from OuterRail.models.location import Location


class ContactRead(BaseModel):
    platform: Optional[Annotated[str, Field(strict=True, max_length=64)]] = Field(
        None,
        description="The platform from which this resource originates. Defaults to `aiod` for assets registered directly on AI-on-Demand. This field should only be set by connectors, leave empty for users submitting assets. If platform is not None, `platform_resource_identifier` should also be set.",)
    platform_resource_identifier: Optional[Annotated[str, Field(strict=True, max_length=256)]] = Field(
        None,
        description="The identifier by which the external platform (from `platform`) identifies the asset. Defaults to the asset identifier for assets registered directly on AIoD. This field should only be set by connectors, leave empty for users submitting assets. ",)
    name: Optional[Annotated[str, Field(strict=True, max_length=256)]] = Field(
        None,
        description="The name of this contact, especially useful if it is not known whether this contact is a person or organisation. For persons, it is preferred to store this information as contact.person.surname and contact.person.firstname. For organisations, store it as contact.organisation.legal_name.",)
    aiod_entry: Optional[AIoDEntryRead] = Field(None, examples=[None], title="Aiod Entry")
    email: Optional[List[str]] = Field(
        None, description="An email address.", examples=[[]], title="Email"
    )
    location: Optional[List[Location]] = Field(None, examples=[[]], title="Location")
    organisation: Optional[StrictStr]
    person: Optional[StrictStr] = Field(None, examples=[None], title="Person")
    telephone: Optional[List[StrictStr]] = Field(None, description="A telephone number, including the land code.",)
    identifier:  Annotated[str, Field(strict=True, max_length=30) ]= Field(..., title="Identifier")
