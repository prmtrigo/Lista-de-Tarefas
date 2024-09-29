from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from pydantic import BaseModel
from typing import Optional

# TABELA TAREFA
class TarefaDB(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, index=True)
    descricao = Column(String, index=True)
    concluida = Column(Boolean, default=False)

# DEFININDO UMA TAREFA
class Tarefa(BaseModel):
    id: Optional[int] = None
    nome: str
    descricao: Optional[str] = None
    concluida: Optional[bool] = False

    class Config:
        orm_mode = True