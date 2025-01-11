from pydantic import BaseModel
from typing import Optional

class ProcessamentoAmericanasResponse(BaseModel):
    id: int
    control: str
    cultivar: str
    ano: int
    kg: Optional[float]

    class Config:
        orm_mode = True
