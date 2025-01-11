from pydantic import BaseModel
from typing import Optional

class ExportacaoEspumantesResponse(BaseModel):
    id: int
    pais: str
    ano: int
    quantidade_kg: Optional[float]
    valor_usd: Optional[float]

    class Config:
        from_attributes = True
