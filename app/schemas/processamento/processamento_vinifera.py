from pydantic import BaseModel
from typing import Optional

class ProcessamentoViniferaResponse(BaseModel):
    id: int
    control: str
    cultivar: str
    ano: int
    valor: Optional[float]

    class Config:
        orm_mode = True
