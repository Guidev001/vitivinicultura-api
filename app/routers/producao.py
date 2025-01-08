from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from app.database.db import SessionLocal
from app.models.producao import Producao
from app.schemas.producao import ProducaoResponse  # Importa o schema Pydantic

router = APIRouter(
    prefix="/api/producao",
    tags=["Produção"],
    responses={404: {"description": "Não encontrado"}},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ProducaoResponse])
def listar_producao(
    id: Optional[int] = Query(None, description="ID do registro"),
    vinhoId: Optional[int] = Query(None, description="ID do vinho"),
    ano: Optional[int] = Query(None, description="Ano do registro"),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(Producao)

        if id:
            query = query.filter(Producao.id == id)

        if vinhoId:
            query = query.filter(Producao.vinho_id == vinhoId)

        if ano:
            query = query.filter(Producao.ano == ano)

        resultados = query.all()
        if not resultados:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado")

        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
