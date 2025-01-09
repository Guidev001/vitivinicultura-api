from fastapi import FastAPI
from app.database.db import Base, engine
from app.routers import producao, comercio, processamento
from app.tasks.scheduler import start_scheduler

Base.metadata.create_all(bind=engine)

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
app.include_router(comercio.router)
app.include_router(processamento.router)

# Iniciar o scheduler
start_scheduler()

@app.get("/")
def read_root():
    return {"message": "API de Produção e Comércio está rodando!"}
