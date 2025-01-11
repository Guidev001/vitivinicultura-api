from sqlalchemy import Column, Integer, String, Float, PrimaryKeyConstraint

from app.models.base import BaseModel


class ImportacaoPassas(BaseModel):
    __tablename__ = "importacao_passas"

    id = Column(Integer, nullable=False)
    pais = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    quantidade_kg = Column(Float, nullable=True)
    valor_usd = Column(Float, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint('id', 'ano'),
    )
