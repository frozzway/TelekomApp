from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    refresh_token: str


class Login(BaseModel):
    username: EmailStr
    password: str


class UserJWT(BaseModel):
    id: int
    roles: list[str]
