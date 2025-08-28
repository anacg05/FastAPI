from fastapi import FastAPI, HTTPException, status, Response, Depends
from models import PersonagensToyStory
from typing import Optional, Any
from routes import curso_router, usuario_router
import requests

app = FastAPI(title = " API dos Personagens de Toy Story - DS18", version = "0.0.1", description="Uma API feita com a ds18 para aprender FastAPI")

app.include_router(curso_router.router, tags=["Cursos"])
app.include_router(usuario_router.router, tags=["Usuarios"])

@app.get("/pokemon/{name}")
def get_pokemon(name: str):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    if response.status_code == 200:
        return response.json()
    return {"Message": "Pokemon not found"}

def fake_db():
    try:
        print("Conectando com o banco")
    finally:
        print("Fechando o banco")

personagens = {
    1: {
        "nome": "Woody",
        "dono": "Andy",
        "tamanho": "Pequeno",
        "foto": "https://static.wikia.nocookie.net/disneyclassicosshow/images/5/50/Toy-story3-creador-de-imagenes_%287%29.jpg/revision/latest?cb=20101201190022&path-prefix=pt-br"
    },

    2: {
        "nome": "Buzz Lighter",
        "dono": "Bonnie",
        "tamanho": "Pequeno",
        "foto": "https://static.wikia.nocookie.net/herois/images/b/bc/BuzzLightyearTS4.webp/revision/latest/thumbnail/width/360/height/360?cb=20220621004845&path-prefix=pt-br"
    }
}


@app.get("/")

 # para criar funções assíncronas
async  def raiz():
    return {"Mensagem":" Funcionou / atualizou"}


@app.get("/personagens")
async  def get_personagens(db: Any = Depends(fake_db)):
    return personagens


@app.get("/personagens/{personagem_id}", description="Retorna um personagem com um id especifico", summary="Retorna um personagem")
async def get_personagem_por_id(personagem_id: int):
    try:
        personagem = personagens[personagem_id]
        return personagem
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontado")


@app.post("/personagens", status_code=status.HTTP_201_CREATED)
async def post_personagem(personagem: Optional[PersonagensToyStory] = None):
    next_id = len(personagens) + 1 
    personagens[next_id] = personagem
    del personagem.id
    return personagem


@app.put("/personagens/{personagem_id}", status_code=status.HTTP_202_ACCEPTED)
async def put_personagem(personagem_id:int, personagem: PersonagensToyStory):
    if personagem_id in personagens:
        personagens[personagem_id] = personagem
        personagem.id = personagem_id
        del personagem.id
        return personagem
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")


@app.delete("/personagens/{personagem_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_personagem(personagem_id: int):
    if personagem_id in personagens:
        del personagens[personagem_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")

@app.get("/calcular")
async def calcular(a: int, b: int):
    
    soma = a+b
    return {"Resultado": soma}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8002, log_level="info", reload=True)

