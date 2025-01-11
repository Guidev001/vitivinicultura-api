from pydantic import BaseModel
from typing import Optional

class ImportacaoFrescasResponse(BaseModel):
    id: int
    pais: str
    ano: int
    quantidade_kg: Optional[float]  # Anotação de tipo explícita
    valor_usd: Optional[float]  # Anotação de tipo explícita

    class Config:
        from_attributes = True  # Substitui orm_mode no Pydantic 2
