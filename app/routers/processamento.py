from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database.db import SessionLocal
from app.models.processamento.processamento_americanas import ProcessamentoAmericanas
from app.models.processamento.processamento_sem_classificacao import ProcessamentoSemClassificacao
from app.models.processamento.processamento_uvas_mesa import ProcessamentoUvasMesa
from app.models.processamento.processamento_vinifera import ProcessamentoVinifera
from app.schemas.processamento.processamento_americanas import ProcessamentoAmericanasResponse
from app.schemas.processamento.processamento_sem_classificacao import ProcessamentoSemClassificacaoResponse
from app.schemas.processamento.processamento_uvas_mesa import ProcessamentoUvasMesaResponse
from app.schemas.processamento.processamento_vinifera import ProcessamentoViniferaResponse

router = APIRouter(
    prefix="/api/processamento",
    tags=["Processamento"],
    responses={404: {"description": "Não encontrado"}},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Processamento - Viníferas
@router.get("/vinifera", response_model=List[ProcessamentoViniferaResponse])
def listar_processamento_vinifera(
    id: Optional[int] = Query(None, description="ID do registro"),
    ano: Optional[int] = Query(None, description="Ano do registro"),
    db: Session = Depends(get_db),
):
    query = db.query(ProcessamentoVinifera)

    if id:
        query = query.filter(ProcessamentoVinifera.id == id)

    if ano:
        query = query.filter(ProcessamentoVinifera.ano == ano)

    return query.all()

# Processamento - Americanas e Híbridas
@router.get("/americanas", response_model=List[ProcessamentoAmericanasResponse])
def listar_processamento_americanas(
    id: Optional[int] = Query(None, description="ID do registro"),
    ano: Optional[int] = Query(None, description="Ano do registro"),
    db: Session = Depends(get_db),
):
    query = db.query(ProcessamentoAmericanas)

    if id:
        query = query.filter(ProcessamentoAmericanas.id == id)

    if ano:
        query = query.filter(ProcessamentoAmericanas.ano == ano)

    return query.all()

# Processamento - Uvas de Mesa
@router.get("/uvas-de-mesa", response_model=List[ProcessamentoUvasMesaResponse])
def listar_processamento_uvas_mesa(
    id: Optional[int] = Query(None, description="ID do registro"),
    ano: Optional[int] = Query(None, description="Ano do registro"),
    db: Session = Depends(get_db),
):
    query = db.query(ProcessamentoUvasMesa)

    if id:
        query = query.filter(ProcessamentoUvasMesa.id == id)

    if ano:
        query = query.filter(ProcessamentoUvasMesa.ano == ano)

    return query.all()

# Processamento - Sem Classificação
@router.get("/sem-classificacao", response_model=List[ProcessamentoSemClassificacaoResponse])
def listar_processamento_sem_classificacao(
    id: Optional[int] = Query(None, description="ID do registro"),
    ano: Optional[int] = Query(None, description="Ano do registro"),
    db: Session = Depends(get_db),
):
    query = db.query(ProcessamentoSemClassificacao)

    if id:
        query = query.filter(ProcessamentoSemClassificacao.id == id)

    if ano:
        query = query.filter(ProcessamentoSemClassificacao.ano == ano)

    return query.all()
