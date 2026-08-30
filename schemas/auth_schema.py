from pydantic import BaseModel, EmailStr, Field


class ResetPasswordRequest(BaseModel): 
    email: EmailStr 
    new_password: str = Field(min_length=8, max_length=128)


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
