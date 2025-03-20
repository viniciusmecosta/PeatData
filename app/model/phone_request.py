from pydantic import BaseModel

class PhoneRequest(BaseModel):
    name: str
    number: str
