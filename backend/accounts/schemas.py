from pydantic import BaseModel


class EmployeeBase(BaseModel):
    name: str
    email: str


class EmployeeCreate(EmployeeBase):
    password: str


class Employee(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True