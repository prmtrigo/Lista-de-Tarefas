from fastapi import FastAPI
from app.database import Base, engine
from app.routes import router as tarefas_router

# CRIANDO TABELA
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ENDPOINT RAIZ
@app.get("/")
async def read_root():
    return {"message": "Bem-vindo à API de Tarefas!"}

# Registrar as rotas
app.include_router(tarefas_router)