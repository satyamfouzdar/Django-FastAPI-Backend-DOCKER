from pydantic import BaseModel


class EmployeeBase(BaseModel):
    name: str
    email: str


class EmployeeCreate(EmployeeBase):
    password: str


class EmployeeLogin(BaseModel):
    email: str
    password: str


class Employee(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class Profile(BaseModel):
    alternate_email: str

    class Config:
        orm_mode = True