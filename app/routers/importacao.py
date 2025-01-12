from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database.db import SessionLocal, get_db
from app.models.importacao.importacao_espumantes import ImportacaoEspumantes
from app.models.importacao.importacao_frescas import ImportacaoFrescas
from app.models.importacao.importacao_passas import ImportacaoPassas
from app.models.importacao.importacao_suco import ImportacaoSuco
from app.models.importacao.importacao_vinhos import ImportacaoVinhos
from app.schemas.importacao.importacao_espumantes import ImportacaoEspumantesResponse
from app.schemas.importacao.importacao_frescas import ImportacaoFrescasResponse
from app.schemas.importacao.importacao_passas import ImportacaoPassasResponse
from app.schemas.importacao.importacao_suco import ImportacaoSucoResponse
from app.schemas.importacao.importacao_vinhos import ImportacaoVinhosResponse

router = APIRouter(
    prefix="/api/importacao",
    tags=["Importação"],
    responses={404: {"description": "Não encontrado"}},
)

# Importação - Vinhos
@router.get("/vinhos", response_model=List[ImportacaoVinhosResponse])
def listar_importacao_vinhos(
    id: Optional[int] = Query(None, description="ID do registro"),
    ano: Optional[int] = Query(None, description="Ano do registro"),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(ImportacaoVinhos)

        if id:
            query = query.filter(ImportacaoVinhos.id == id)

        if ano:
            query = query.filter(ImportacaoVinhos.ano == ano)

        resultados = query.all()
        if not resultados:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado")

        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Importação - Sucos
@router.get("/sucos", response_model=List[ImportacaoSucoResponse])
def listar_importacao_sucos(
    id: Optional[int] = Query(None, description="ID do registro"),
    ano: Optional[int] = Query(None, description="Ano do registro"),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(ImportacaoSuco)

        if id:
            query = query.filter(ImportacaoSuco.id == id)

        if ano:
            query = query.filter(ImportacaoSuco.ano == ano)

        resultados = query.all()
        if not resultados:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado")

        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Importação - Passas
@router.get("/passas", response_model=List[ImportacaoPassasResponse])
def listar_importacao_passas(
    id: Optional[int] = Query(None, description="ID do registro"),
    ano: Optional[int] = Query(None, description="Ano do registro"),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(ImportacaoPassas)

        if id:
            query = query.filter(ImportacaoPassas.id == id)

        if ano:
            query = query.filter(ImportacaoPassas.ano == ano)

        resultados = query.all()
        if not resultados:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado")

        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Importação - Frescas
@router.get("/frescas", response_model=List[ImportacaoFrescasResponse])
def listar_importacao_frescas(
    id: Optional[int] = Query(None, description="ID do registro"),
    ano: Optional[int] = Query(None, description="Ano do registro"),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(ImportacaoFrescas)

        if id:
            query = query.filter(ImportacaoFrescas.id == id)

        if ano:
            query = query.filter(ImportacaoFrescas.ano == ano)

        resultados = query.all()
        if not resultados:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado")

        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Importação - Espumantes
@router.get("/espumantes", response_model=List[ImportacaoEspumantesResponse])
def listar_importacao_espumantes(
    id: Optional[int] = Query(None, description="ID do registro"),
    ano: Optional[int] = Query(None, description="Ano do registro"),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(ImportacaoEspumantes)

        if id:
            query = query.filter(ImportacaoEspumantes.id == id)

        if ano:
            query = query.filter(ImportacaoEspumantes.ano == ano)

        resultados = query.all()
        if not resultados:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado")

        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))