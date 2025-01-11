from sqlalchemy import Column, Integer, String, Float, PrimaryKeyConstraint
from sqlalchemy.orm import validates

from app.database.db import Base
from app.models.base import BaseModel


class ProcessamentoAmericanas(BaseModel):
    __tablename__ = "processamento_americanas"

    id = Column(Integer, nullable=False)
    control = Column(String, nullable=False)
    cultivar = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    kg = Column(Float, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint('id', 'ano'),
    )