
from fastapi import FastAPI, status, Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import Optional
#from sqlmodel import Field, SQLModel


API_KEY = '123asd'
API_KEY_HEADER = 'AUTHORIZATION'
api_key_header_auth = APIKeyHeader(name=API_KEY_HEADER, auto_error=True)

def get_api_key(api_key_header = Security(api_key_header_auth)):
    if api_key_header != API_KEY:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail='Invalid API Key',
        )




app = FastAPI()



class Produto(BaseModel):
    id: Optional[int] = 0
    nome: str
    preco: float
    desc: Optional[str] = None


db_produtos = [
    Produto(id=1, nome='caneta azul', preco = 1.50, desc='Bic'),
    Produto(id=2, nome='caneta preta', preco = 1.50),
    Produto(id=3, nome='caneta vermelha', preco = 2.00),
    Produto(id=4, nome='caneta verde', preco = 2.00),
]






@app.get('/')
async def home():
    return {'Mensagem': 'Api de produtos by Guilherme'}


@app.get('/produtos/me')
async def mostrarproduto():
    return{'Produto': 'Eu sou eum produto'}



@app.get('/produtos/', dependencies=[Security(get_api_key)])
async def exibir_produtos():
    return {'produto': db_produtos, 'data': 'Conteúdo Seguro!!'}


@app.get('/produtos/{id}')
async def mostrar_produto(id: int):
    return {'produto': [produto for produto in db_produtos if produto.id==id]}


@app.post('/produtos', status_code=status.HTTP_201_CREATED)
async def criar_produto(produto: Produto):
    produto.id = db_produtos[-1].id + 1
    db_produtos.append(produto)
    return {'Mensagem': 'Produto criado!'}


@app.patch('/produtos/{id}')
async def atualizar_produto(id: int, produto: Produto):
    index = [index for index, produto in enumerate(db_produtos) if produto.id == id]
    produto.id = db_produtos[index[0]].id
    db_produtos[index[0]] = produto
    return {'Mensagem': 'Produto atualizado!'}


@app.delete('/produtos/{id}')
async def apagar_produto(id: int):
    produto = [produto for produto in db_produtos if produto.id == id]  
    db_produtos.remove(produto[0])
    return {'Mensagem': 'Produto excluído!'}




'''uvicorn main:app --reload'''