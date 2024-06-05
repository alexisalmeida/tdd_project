import uuid
from datetime import datetime

from pydantic import BaseModel, UUID4, Field


class CreateBaseModel(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    """
    @model_serializer
    def set_model(self) -> dict[str, Any]:
        self_dict = dict(self)
        for key, value in self_dict.items():
                self_dict[key] = Decimal128(value)

        return self_dict
    """
