from fastapi import FastAPI

from app.database.db import Base, engine
from app.routers import producao
from app.tasks.scheduler import start_scheduler

# Inicializar o banco de dados
Base.metadata.create_all(bind=engine)

# Iniciar a aplicação FastAPI
app = FastAPI(
    title="Vitivinicultura API",
    description="API para gerenciar dados de vitivinicultura.",
    version="1.0.0",
    contact={
        "name": "Guilherme Gomes David",
        "email": "guidev001@gmail.com",
    },
    license_info={
        "name": "MIT License",
    },
)

app.include_router(producao.router)

# Iniciar o agendador de tarefas
# start_scheduler()

@app.get("/")
def read_root():
    return {"message": "API de Produção está rodando!"}
