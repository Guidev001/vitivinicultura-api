from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from app.auth.auth_service import authenticate_user
from app.database.db import Base, engine, get_db
from app.routers import producao, comercio, processamento, importacao, users, exportacao
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

@app.middleware("http")
async def basic_auth_middleware(request: Request, call_next):
    open_paths = ["/users/", "/users"]

    if not any(request.url.path.startswith(path) for path in open_paths):
        try:
            db = next(get_db())
            await authenticate_user(request, db)
        except HTTPException as exc:
            return JSONResponse(
                content={"detail": exc.detail},
                status_code=exc.status_code,
                headers={"WWW-Authenticate": "Basic"}
            )
    response = await call_next(request)
    return response


app.include_router(producao.router)
app.include_router(comercio.router)
app.include_router(processamento.router)
app.include_router(importacao.router)
app.include_router(exportacao.router)
app.include_router(users.router)

start_scheduler()

@app.get("/")
def read_root():
    return {"message": "API de Produção e Comércio está rodando!"}
