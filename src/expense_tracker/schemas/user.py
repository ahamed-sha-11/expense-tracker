from pydantic import BaseModel, EmailStr, Field, field_validator

from expense_tracker.core.config import ALLOWED_PASSWORD_CHARACTERS


class UserResponse(BaseModel):
    username: str
    email: EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=20)

    @field_validator("password")
    @classmethod
    def check_password_characters(cls, password: str) -> str:
        for character in password:
            if character not in ALLOWED_PASSWORD_CHARACTERS:
                raise ValueError("Password can only contain letters, digits and symbols like !@#$%^&*")
        return password
