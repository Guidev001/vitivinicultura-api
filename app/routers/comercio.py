from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from app.database.db import SessionLocal
from app.models.comercio import Comercio
from app.schemas.comercio import ComercioResponse

router = APIRouter(
    prefix="/api/comercio",
    tags=["Comércio"],
    responses={404: {"description": "Não encontrado"}},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ComercioResponse])
def listar_producao(
    id: Optional[int] = Query(None, description="ID do registro"),
    vinhoId: Optional[int] = Query(None, description="ID do vinho"),
    ano: Optional[int] = Query(None, description="Ano do registro"),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(Comercio)

        if id:
            query = query.filter(Comercio.id == id)

        if vinhoId:
            query = query.filter(Comercio.vinho_id == vinhoId)

        if ano:
            query = query.filter(Comercio.ano == ano)

        resultados = query.all()
        if not resultados:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado")

        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
