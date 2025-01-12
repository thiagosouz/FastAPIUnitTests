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

def test_deve_listar_contas_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    client.post("/contas-a-pagar-e-receber", json={'descricao': 'Aluguel', 'valor': 2500.0, 'tipo': 'PAGAR'})
    client.post("/contas-a-pagar-e-receber", json={'descricao': 'Salário', 'valor': 5000.0, 'tipo': 'RECEBER'})
    
    response = client.get("/contas-a-pagar-e-receber")
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'descricao': 'Aluguel', 'valor': '2500.0000000000', 'tipo': 'PAGAR'},
        {'id': 2, 'descricao': 'Salário', 'valor': '5000.0000000000', 'tipo': 'RECEBER'}
    ]
    
def test_deve_criar_contas_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    nova_conta = {
        "descricao": "Teste de criacao de conta",
        "valor": 100,
        "tipo": "PAGAR"
    }
    nova_conta_copy = nova_conta.copy()
    nova_conta_copy["id"] = 1

    response = client.post("/contas-a-pagar-e-receber", json=nova_conta)
    assert response.status_code == 201

    response_data = response.json()
    response_data["valor"] = float(response_data["valor"])
    assert response_data == nova_conta_copy
    
def test_deve_retornar_erro_excecao_caracteres_descricao():
    response = client.post("/contas-a-pagar-e-receber", json={
        'descricao': '1234567891012345678912345678903',
        'valor': 2000.0,
        'tipo': 'RECEBER'
    })
    assert response.status_code == 422
    
def test_deve_retornar_erro_excecao_caracteres_descricao_menor_que_necessario():
    response = client.post("/contas-a-pagar-e-receber", json={
        'descricao': '12',
        'valor': 1200.0,
        'tipo': 'RECEBER'
    })
    assert response.status_code == 422
    
def test_deve_retornar_erro_valor_for_zero_ou_menor():
    response = client.post("/contas-a-pagar-e-receber", json={
        'descricao': 'Teste',
        'valor': 0,
        'tipo': 'RECEBER'
    })
    assert response.status_code == 422
    
    response = client.post("/contas-a-pagar-e-receber", json={
        'descricao': 'Teste',
        'valor': -1,
        'tipo': 'RECEBER'
    })
    assert response.status_code == 422
    
def test_deve_retornar_erro_tipo_for_invalido():
    response = client.post("/contas-a-pagar-e-receber", json={
        'descricao': 'Teste',
        'valor': 50,
        'tipo': 'NADA'
    })
    assert response.status_code == 422    
    