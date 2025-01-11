from pydantic import BaseModel
from typing import Optional

class ProcessamentoSemClassificacaoResponse(BaseModel):
    id: int
    control: str
    cultivar: str
    ano: int
    kg: Optional[float]

    class Config:
        orm_mode = True
