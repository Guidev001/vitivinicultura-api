from math import isnan

from sqlalchemy.orm import validates
from app.database.db import Base

class BaseModel(Base):
    __abstract__ = True

    @validates("valor")
    def validate_valor(self, key, value):
        """
        Valida o campo 'valor'. Converte valores inválidos para None.
        """
        if value is None:
            return None
        if isinstance(value, float) and isnan(value):  # Detecta NaN explícito
            return None
        if isinstance(value, str) and value.strip().lower() in ["nd", "t", "na", "nan"]:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            print(f"Erro ao converter {value}. Substituindo por None.")
            return None
