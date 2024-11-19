from typing import Annotated
from pydantic import BaseModel, Field
from ..core.schemas import TimestampSchema, UUIDSchema

url_regex_field = Field(..., description="The URL regex of the trigger", pattern=r"^https?://.*$", examples=[".*", "https://example.com", "https://example.com/.*"])
name_field = Field(..., description="The name of the trigger")

class TriggerBase(BaseModel):
    url_regex: Annotated[str, url_regex_field]
    name: Annotated[str, name_field]

class Trigger(TriggerBase, UUIDSchema, TimestampSchema):
    pass
class TriggerRead(Trigger):
    pass

class TriggerCreate(TriggerBase):
    url_regex: Annotated[str, url_regex_field]
    name: Annotated[str, name_field]

class TriggerUpdate(TriggerBase):
    url_regex: Annotated[str, url_regex_field]
    name: Annotated[str, name_field]

class TriggerDelete(UUIDSchema):
    pass

