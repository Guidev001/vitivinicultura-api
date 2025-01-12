from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from app.database.db import SessionLocal, get_db

from app.models.producao.producao import Producao
from app.schemas.producao.producao import ProducaoResponse

router = APIRouter(
    prefix="/api/producao",
    tags=["Produção"],
    responses={404: {"description": "Não encontrado"}},
)

@router.get("/", response_model=List[ProducaoResponse])
def listar_producao(
    id: Optional[int] = Query(None, description="ID do registro"),
    ano: Optional[int] = Query(None, description="Ano do registro"),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(Producao)

        if id:
            query = query.filter(Producao.id == id)

        if ano:
            query = query.filter(Producao.ano == ano)

        resultados = query.all()
        if not resultados:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado")

        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
