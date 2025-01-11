from pydantic import BaseModel
from typing import Optional

class ProducaoResponse(BaseModel):
    id: int
    control: str
    produto: str
    ano: int
    litros: Optional[float]

    class Config:
        orm_mode = True
