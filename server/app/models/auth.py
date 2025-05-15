from pydantic import BaseModel, EmailStr, UUID4


class Token(BaseModel):
    access_token: str
    refresh_token: str


class Login(BaseModel):
    username: EmailStr
    password: str


class UserJWT(BaseModel):
    id: UUID4
    roles: list[str]
