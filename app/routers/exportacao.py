from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database.db import SessionLocal
from app.models.exportacao.exportacao_espumantes import ExportacaoEspumantes
from app.models.exportacao.exportacao_frescas import ExportacaoFrescas
from app.models.exportacao.exportacao_suco import ExportacaoSuco
from app.models.exportacao.exportacao_vinhos import ExportacaoVinhos
from app.models.importacao.importacao_espumantes import ImportacaoEspumantes
from app.models.importacao.importacao_frescas import ImportacaoFrescas
from app.models.importacao.importacao_passas import ImportacaoPassas
from app.models.importacao.importacao_suco import ImportacaoSuco
from app.models.importacao.importacao_vinhos import ImportacaoVinhos
from app.schemas.exportacao.exportacao_espumantes import ExportacaoEspumantesResponse
from app.schemas.exportacao.exportacao_frescas import ExportacaoFrescasResponse
from app.schemas.exportacao.exportacao_suco import ExportacaoSucoResponse
from app.schemas.exportacao.exportacao_vinhos import ExportacaoVinhosResponse
from app.schemas.importacao.importacao_espumantes import ImportacaoEspumantesResponse
from app.schemas.importacao.importacao_frescas import ImportacaoFrescasResponse
from app.schemas.importacao.importacao_passas import ImportacaoPassasResponse
from app.schemas.importacao.importacao_suco import ImportacaoSucoResponse
from app.schemas.importacao.importacao_vinhos import ImportacaoVinhosResponse

router = APIRouter(
    prefix="/api/exportacao",
    tags=["Exportação"],
    responses={404: {"description": "Não encontrado"}},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Importação - Vinhos
@router.get("/vinhos", response_model=List[ExportacaoVinhosResponse])
def listar_exportacao_vinhos(
    id: Optional[int] = Query(None, description="ID do registro"),
    ano: Optional[int] = Query(None, description="Ano do registro"),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(ExportacaoVinhos)

        if id:
            query = query.filter(ExportacaoVinhos.id == id)

        if ano:
            query = query.filter(ExportacaoVinhos.ano == ano)

        resultados = query.all()
        if not resultados:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado")

        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Importação - Sucos
@router.get("/sucos", response_model=List[ExportacaoSucoResponse])
def listar_exportacao_sucos(
    id: Optional[int] = Query(None, description="ID do registro"),
    ano: Optional[int] = Query(None, description="Ano do registro"),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(ExportacaoSuco)

        if id:
            query = query.filter(ExportacaoSuco.id == id)

        if ano:
            query = query.filter(ExportacaoSuco.ano == ano)

        resultados = query.all()
        if not resultados:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado")

        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Importação - Frescas
@router.get("/frescas", response_model=List[ExportacaoFrescasResponse])
def listar_exportacao_frescas(
    id: Optional[int] = Query(None, description="ID do registro"),
    ano: Optional[int] = Query(None, description="Ano do registro"),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(ExportacaoFrescas)

        if id:
            query = query.filter(ExportacaoFrescas.id == id)

        if ano:
            query = query.filter(ExportacaoFrescas.ano == ano)

        resultados = query.all()
        if not resultados:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado")

        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Importação - Espumantes
@router.get("/espumantes", response_model=List[ExportacaoEspumantesResponse])
def listar_exportacao_espumantes(
    id: Optional[int] = Query(None, description="ID do registro"),
    ano: Optional[int] = Query(None, description="Ano do registro"),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(ExportacaoEspumantes)

        if id:
            query = query.filter(ExportacaoEspumantes.id == id)

        if ano:
            query = query.filter(ExportacaoEspumantes.ano == ano)

        resultados = query.all()
        if not resultados:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado")

        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))