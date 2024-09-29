from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import TarefaDB, Tarefa
from app.database import get_db

router = APIRouter()

# CRIANDO TAREFA
@router.post("/tarefas/", response_model=Tarefa)
async def criar_tarefa(tarefa: Tarefa, db: Session = Depends(get_db)):
    db_tarefa = TarefaDB(nome=tarefa.nome, descricao=tarefa.descricao, concluida=tarefa.concluida)
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

# LISTAR TAREFAS
@router.get("/tarefas/", response_model=list[Tarefa])
async def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(TarefaDB).all()

# LISTAR TAREFAS CONCLUÍDAS
@router.get("/tarefas/concluidas/", response_model=list[Tarefa])
async def listar_tarefas_concluidas(db: Session = Depends(get_db)):
    return db.query(TarefaDB).filter(TarefaDB.concluida == True).all()

# OBTER TAREFA POR ID
@router.get("/tarefas/{tarefa_id}", response_model=Tarefa)
async def obter_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(TarefaDB).filter(TarefaDB.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

# ATUALIZAR TAREFA
@router.put("/tarefas/{tarefa_id}", response_model=Tarefa)
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
@router.delete("/tarefas/{tarefa_id}")
async def excluir_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(TarefaDB).filter(TarefaDB.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    db.delete(tarefa)
    db.commit()
    return {"message": "Tarefa excluída com sucesso"}
