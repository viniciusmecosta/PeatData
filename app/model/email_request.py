from pydantic import BaseModel


class EmailRequest(BaseModel):
    name: str
    email: str
