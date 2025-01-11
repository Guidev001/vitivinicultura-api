from sqlalchemy import Column, Integer, String, Float, PrimaryKeyConstraint

from app.database.db import Base

class Comercio(Base):
    __tablename__ = "comercio"

    id = Column(Integer, nullable=False)
    control = Column(String, nullable=True)
    produto = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    litros = Column(Float, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint('id', 'ano'),
    )