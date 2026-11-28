from pydantic import BaseModel, Field, field_validator


class LLMCredentialCreate(BaseModel):
    # Sent in the request body, never in the URL, so the key does not end up in logs or browser history.
    # At least 12 characters, so the masked key always hides some of it (it shows only the first 4 and last 4).
    api_key: str = Field(min_length=12, max_length=500)
    model: str = Field(min_length=1, max_length=100)


class LLMCredentialUpdate(BaseModel):
    # Send only the fields you want to change. Same limits as when saving.
    api_key: str | None = Field(default=None, min_length=12, max_length=500)
    model: str | None = Field(default=None, min_length=1, max_length=100)
    is_active: bool | None = None

    @field_validator("api_key", "model", "is_active")
    @classmethod
    def reject_null(cls, value):
        if value is None:
            raise ValueError("Can't be empty. Leave the field out to keep its current value")
        return value


class LLMCredentialResponse(BaseModel):
    id: int
    masked_key: str
    model: str
    is_active: bool
