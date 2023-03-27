from pydantic import BaseModel


class Country(BaseModel):
    """
    Schema for Country
    """
    name: str

    class Config:
        orm_mode = True


class Institution(BaseModel):
    """
    Schema for Institution
    """
    name: str
    logo: str

    class Config:
        orm_mode = True