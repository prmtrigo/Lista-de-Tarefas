from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Banco de Dados
SQLALCHEMY_DATABASE_URL = "sqlite:///tarefas.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# TABELA TAREFA
class TarefaDB(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, index=True)
    descricao = Column(String, index=True)
    concluida = Column(Boolean, default=False)

# CRIANDO TABELA
Base.metadata.create_all(bind=engine)

app = FastAPI()

# DEFININDO UMA TAREFA
class Tarefa(BaseModel):
    id: Optional[int] = None
    nome: str
    descricao: Optional[str] = None
    concluida: Optional[bool] = False

    class Config:
        orm_mode = True

# ENDPOINT RAIZ
@app.get("/")
async def read_root():
    return {"message": "Bem-vindo à API de Tarefas!"}

# OBTER NO BANCO DE DADOS
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRIANDO TAREFA
@app.post("/tarefas/", response_model=Tarefa)
async def criar_tarefa(tarefa: Tarefa, db: Session = Depends(get_db)):
    db_tarefa = TarefaDB(nome=tarefa.nome, descricao=tarefa.descricao, concluida=tarefa.concluida)
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

# LISTAR TAREFAS
@app.get("/tarefas/", response_model=List[Tarefa])
async def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(TarefaDB).all()

# LISTAR TAREFAS CONCLUÍDAS
@app.get("/tarefas/concluidas/", response_model=List[Tarefa])
async def listar_tarefas_concluidas(db: Session = Depends(get_db)):
    return db.query(TarefaDB).filter(TarefaDB.concluida == True).all()

# OBTER TAREFA POR ID
@app.get("/tarefas/{tarefa_id}", response_model=Tarefa)
async def obter_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(TarefaDB).filter(TarefaDB.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

# ATUALIZAR TAREFA
@app.put("/tarefas/{tarefa_id}", response_model=Tarefa)
async def atualizar_tarefa(tarefa_id: int, nova_tarefa: Tarefa, db: Session = Depends(get_db)):
    tarefa = db.query(TarefaDB).filter(TarefaDB.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    tarefa.nome = nova_tarefa.nome
    tarefa.descricao = nova_tarefa.descricao
    tarefa.concluida = nova_tarefa.concluida
    db.commit()
    db.refresh(tarefa)
    return tarefa

# EXCLUIR TAREFA
@app.delete("/tarefas/{tarefa_id}")
async def excluir_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(TarefaDB).filter(TarefaDB.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    db.delete(tarefa)
    db.commit()
    return {"message": "Tarefa excluída com sucesso"}