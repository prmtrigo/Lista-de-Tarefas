import pytest
from fastapi.testclient import TestClient
from main import app, Tarefa 

client = TestClient(app)

# CRIAR UMA TAREFA
def test_criar_tarefa():
    response = client.post("/tarefas/", json={
        "nome": "Tarefa 1", 
        "descricao": "Descrição da tarefa 1"
        })
    assert response.status_code == 200
    assert response.json()["nome"] == "Tarefa 1"
    assert response.json()["descricao"] == "Descrição da tarefa 1"
    assert response.json()["concluida"] is False

# LISTAR TAREFAS
def test_listar_tarefas():
    response = client.get("/tarefas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# OBTER UMA TAREFA POR ID
def test_obter_tarefa():
    criar_response = client.post("/tarefas/", json={"nome": "Tarefa 2"})
    tarefa_id = criar_response.json()["id"]

    response = client.get(f"/tarefas/{tarefa_id}")
    assert response.status_code == 200
    assert response.json()["id"] == tarefa_id
    assert response.json()["nome"] == "Tarefa 2"

# OBTER UMA TAREFA QUE NÃO EXISTE
def test_obter_tarefa_nao_existente():
    response = client.get("/tarefas/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Tarefa não encontrada"}

# ATUALIZAR TAREFA
def test_atualizar_tarefa():
    criar_response = client.post("/tarefas/", json={
        "nome": "Tarefa para Atualizar", 
        "descricao": "Descrição original"
        })
    tarefa_id = criar_response.json()["id"]

    atualizar_response = client.put(f"/tarefas/{tarefa_id}", json={
        "nome": "Tarefa Atualizada", 
        "descricao": "Nova descrição",
        "concluida": True
    })
    assert atualizar_response.status_code == 200
    assert atualizar_response.json()["id"] == tarefa_id
    assert atualizar_response.json()["nome"] == "Tarefa Atualizada"
    assert atualizar_response.json()["descricao"] == "Nova descrição"
    assert atualizar_response.json()["concluida"] is True

# ATUALIZAR UMA TAREFA QUE NÃO EXISTE
def test_atualizar_tarefa_nao_existente():
    response = client.put("/tarefas/999", json={
        "nome": "Tarefa Atualizada", 
        "descricao": "Nova descrição"
        })
    assert response.status_code == 404
    assert response.json() == {"detail": "Tarefa não encontrada"}

# EXCLUIR TAREFA
def test_excluir_tarefa():
    criar_response = client.post("/tarefas/", json={"nome": "Tarefa 4"})
    tarefa_id = criar_response.json()["id"]

    response = client.delete(f"/tarefas/{tarefa_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Tarefa excluída com sucesso"} 

    response = client.get(f"/tarefas/{tarefa_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Tarefa não encontrada"}

# EXCLUIR UMA TAREFA QUE NÃO EXISTE
def test_excluir_tarefa_nao_existente():
    response = client.delete("/tarefas/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Tarefa não encontrada"}
