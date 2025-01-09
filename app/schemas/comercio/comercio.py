from pydantic import BaseModel
from typing import Optional

class ComercioResponse(BaseModel):
    id: int
    control: Optional[str]
    produto: str
    ano: int
    valor: Optional[float]

    class Config:
        orm_mode = True
