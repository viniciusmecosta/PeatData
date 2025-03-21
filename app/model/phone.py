from pydantic import BaseModel


class Phone(BaseModel):
    name: str
    number: str
    comedouro: str
