from pydantic import BaseModel


class MessageBase(BaseModel):
    id: int
    message: str
    #config attr
    model_config = {"from_attributes": True}
