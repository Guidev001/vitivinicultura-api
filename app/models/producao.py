from sqlalchemy import Column, Integer, String, Float
from app.database.db import Base

class Producao(Base):
    __tablename__ = "producao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vinho_id = Column(Integer, nullable=False)
    control = Column(String, nullable=False)
    produto = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    valor = Column(Float, nullable=True)
