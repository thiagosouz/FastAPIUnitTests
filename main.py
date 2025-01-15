import uvicorn
from fastapi import FastAPI
from contas_a_pagar_e_receber.routers import contas_a_pagar_e_receber_router

app =  FastAPI()

@app.get("/")
def oi_programador():
    return "Olá QA programador! Vamos treinar um projeto construído do 0 com testes unitários! TDD na prática."

app.include_router(contas_a_pagar_e_receber_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)