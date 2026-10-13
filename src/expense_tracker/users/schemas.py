from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    email: EmailStr

class UserResponse(BaseModel):
    username: str
    email: EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(min_length=8, max_length=72)
