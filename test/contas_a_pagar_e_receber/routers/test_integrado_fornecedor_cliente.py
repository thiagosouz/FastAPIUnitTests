from shared.database import Base
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shared.dependencies import get_db

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
app.dependency_overrides[get_db] = override_get_db       

def test_deve_listar_fornecedores_clientes():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    client.post("/fornecedor-cliente", json={'nome': 'Alex'})
    client.post("/fornecedor-cliente", json={'nome': 'João'})
    
    response = client.get("/fornecedor-cliente")
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'nome': 'Alex'},
        {'id': 2, 'nome': 'João'}
    ]
    
def test_deve_listar_fornecedor_por_id():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/fornecedor-cliente", json={
        "nome": "Mariano Lage",
    })
    
    id_fornecedor_cliente = response.json()['id']
    
    response_get = client.get(f"/fornecedor-cliente/{id_fornecedor_cliente}")
    
    assert response_get.status_code == 200
    assert response_get.json()['nome'] == 'Mariano Lage'
    
def test_deve_retornar_nao_encontrado_para_fornecedor_inexistente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
        
    response_get = client.get(f"/fornecedor-cliente/1000")
    
    assert response_get.status_code == 404
    
def test_deve_criar_fornecedor():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    novo_fornecedor = {
        "nome": "Carlos Alberto de Nóbrega",
    }
    novo_fornecedor_copy = novo_fornecedor.copy()
    novo_fornecedor_copy["id"] = 1

    response = client.post("/fornecedor-cliente", json=novo_fornecedor)
    assert response.status_code == 201

    response_data = response.json()
    assert response_data == novo_fornecedor_copy
    
def test_deve_atualizar_fornecedor():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/fornecedor-cliente", json={
        "nome": "Daniela Silva",
    })
    
    id_fornecedor_cliente = response.json()['id']
    
    response_put = client.put(f"/fornecedor-cliente/{id_fornecedor_cliente}", json={
        "nome": "Daniela Costa",
    })
    assert response_put.status_code == 200
    assert response_put.json()['nome'] == 'Daniela Costa'
    
def test_deve_retornar_nao_encontrado_para_fornecedor_inexistente_na_atualizacao():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    response_put = client.put(f"/fornecedor-cliente/2000", json={
        "nome": "TAMBASA",
    })
    assert response_put.status_code == 404    
    
def test_deve_deletar_fornecedor():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/fornecedor-cliente", json={
        "nome": "TIM/SA",
    })
    
    id_fornecedor_cliente = response.json()['id']
    
    response_delete = client.delete(f"/fornecedor-cliente/{id_fornecedor_cliente}")
    assert response_delete.status_code == 204
    
def test_deve_retornar_nao_encontrado_para_fornecedor_inexistente_ao_deletar():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    response_delete = client.delete(f"/fornecedor-cliente/2000")
    
    assert response_delete.status_code == 404
    
def test_deve_retornar_erro_excecao_caracteres_nome():
    response = client.post("/fornecedor-cliente", json={
        'nome': '^#$55_7&3!0-107010=3_97-_7-472@-#&%@#8*-=8+*3#2#-=6!4=%1^&#$#7+-*3+=!@^4515^!!--3^=%72+3*!+&=@054#65^#$55_7&3!0-107010=3_97-_7-472@-#&%@#8*-=8+*3#2#-=6!4=%1^&#$#7+-*3+=!@^4515^!!--3^=%72+3*!+&=@054#6558^&=36+#&%97-^9-&29$!_*##@78*!985^3=#7=4=18@9@8+850*=!^',
    })
    assert response.status_code == 422
    
def test_deve_retornar_erro_excecao_caracteres_nome_menor_que_necessario():
    response = client.post("/fornecedor-cliente", json={
        'nome': 'KL',
    })
    assert response.status_code == 422
 
    