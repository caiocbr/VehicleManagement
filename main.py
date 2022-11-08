from typing import Union

from fastapi import FastAPI

app = FastAPI()

# Autenticação
@app.post("/auth")
def read_root():
    pass

# Pedido de veículo
@app.post("/vehicle/request")
def read_item():
    pass

# Consulta de pedido
@app.get("/vehicle/request")
def read_item():
    pass

# Deletar pedido
@app.delete("/vehicle/request")
def read_item():
    pass

# Cadastro viatura
@app.get("/vehicles/sigin")
def read_item():
    pass

# Deletar viatura
@app.delete("/vehicles/delete")
def read_item():
    pass

# Consulta viatura
@app.get("/vehicles/query")
def read_item():
    pass