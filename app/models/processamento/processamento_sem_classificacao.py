from sqlalchemy import Column, Integer, String, Float, PrimaryKeyConstraint
from app.database.db import Base

class ProcessamentoSemClassificacao(Base):
    __tablename__ = "processamento_sem_classificacao"

    id = Column(Integer, nullable=False)
    control = Column(String, nullable=False)
    cultivar = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    valor = Column(Float, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint('id', 'ano'),
    )
