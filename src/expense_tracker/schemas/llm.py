from pydantic import BaseModel, Field


class LLMCredentialCreate(BaseModel):
    # Sent in the request body, never in the URL, so the key does not end up in logs or browser history.
    # At least 12 characters, so the masked key always hides some of it (it shows only the first 4 and last 4).
    api_key: str = Field(min_length=12, max_length=500)
    model: str = Field(min_length=1, max_length=100)


class LLMCredentialResponse(BaseModel):
    id: int
    masked_key: str
    model: str
    is_active: bool
