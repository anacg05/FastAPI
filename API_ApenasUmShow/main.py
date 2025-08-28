from fastapi import FastAPI, HTTPException, status, Response
from typing import Optional

app = FastAPI(
    title="API dos Personagens de Apenas um Show",
    version="1.0.1",
    description="Uma API com personagens de Apenas um Show"
)

# --- Base de personagens como dicionário ---
personagens = {
    1: {"nome": "Mordecai", "espécie": "Pássaro-azul", "imagem": "https://static.wikia.nocookie.net/herois/images/e/e2/Mordecai_McSingleton.png/revision/latest?cb=20221105204753&path-prefix=pt-br"},
    2: {"nome": "Rigby", "espécie": "Guaxinim", "imagem": "https://static.wikia.nocookie.net/apenasumshow/images/d/dd/Rigby.png/revision/latest?cb=20140401235618&path-prefix=pt-br"},
    3: {"nome": "Benson", "espécie": "Máquina de chicletes", "imagem": "https://static.wikia.nocookie.net/apenasumshow/images/b/be/250px-Benson_character.png/revision/latest?cb=20140330023927&path-prefix=pt-br"},
    4: {"nome": "Saltitão", "espécie": "Yeti", "imagem": "https://static.wikia.nocookie.net/apenasumshow/images/d/da/Ss.png/revision/latest?cb=20120411181528&path-prefix=pt-br"},
    5: {"nome": "Pairulito", "espécie": "Homem-pirulito", "imagem": "https://static.wikia.nocookie.net/apenasumshow/images/2/26/Pops_character.png/revision/latest?cb=20131101153117&path-prefix=pt-br"},
    6: {"nome": "Musculoso", "espécie": "Humano verde", "imagem": "https://static.wikia.nocookie.net/apenasumshow/images/c/c7/Musculoso.png/revision/latest?cb=20120123200521&path-prefix=pt-br"},
    7: {"nome": "Fantasmão", "espécie": "Fantasma com mão", "imagem": "https://static.wikia.nocookie.net/herois/images/1/17/Hi_Five_Ghost.png/revision/latest?cb=20221113014548&path-prefix=pt-br"},
    8: {"nome": "Margarete", "espécie": "Pássaro-vermelho (cardeal)", "imagem": "https://static.wikia.nocookie.net/apenasumshow/images/a/ad/Mordecai_e_Margaret.png/revision/latest?cb=20120329202929&path-prefix=pt-br"},
    9: {"nome": "CJ", "espécie": "Nuvem", "imagem": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9xHlvnCOqZiHCdyOkqD67wKGs2AlHbflNs3lvDXwV_iRe7YsFcemAepzpvurrbiw4V8k&usqp=CAU"},
    10: {"nome": "Eileen", "espécie": "Texugo", "imagem": "https://static.wikia.nocookie.net/apenasumshow/images/e/e0/Littlemolegirl.png/revision/latest?cb=20130418211841&path-prefix=pt-br"},
    11: {"nome": "Starla", "espécie": "Humana verde", "imagem": "https://static.wikia.nocookie.net/apenasumshow/images/d/d4/Musculosa_Guts.png/revision/latest?cb=20130824143135&path-prefix=pt-br"},
    12: {"nome": "Thomas", "espécie": "Cabra", "imagem": "https://static.wikia.nocookie.net/herois/images/4/4c/Regular_Show_-_Thomas.png/revision/latest/thumbnail/width/360/height/360?cb=20210921014312&path-prefix=pt-br"},
    13: {"nome": "Don", "espécie": "Guaxinim (irmão do Rigby)", "imagem": "https://images1.wikia.nocookie.net/__cb20101110131419/theregularshow/images/2/24/Don.png"},
    14: {"nome": "Sr. Maellard", "espécie": "Humano (pai do Pairulito)", "imagem": "https://static.wikia.nocookie.net/apenasumshow/images/2/2b/Reg_174x252_mrmaellard.png/revision/latest?cb=20140304111704&path-prefix=pt-br"},
    15: {"nome": "Pai do Musculoso", "espécie": "Fantasma", "imagem": "https://pbs.twimg.com/media/EVVQoqVXkAcnLxv.jpg"}
}

# --- Rotas ---

@app.get("/")
async def raiz():
    return {"Mensagem": "API de Apenas um Show funcionando!"}


@app.get("/personagens/{personagem_id}", description="Retorna um personagem específico", summary="Buscar personagem por ID")
async def get_personagem_por_id(personagem_id: int):
    personagem = personagens.get(personagem_id)
    if personagem:
        return {"id": personagem_id, **personagem}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")


@app.post("/personagens", status_code=status.HTTP_201_CREATED)
async def post_personagem(personagem: Optional[dict] = None):
    next_id = max(personagens.keys(), default=0) + 1
    personagens[next_id] = personagem
    return {"id": next_id, **personagem}


@app.put("/personagens/{personagem_id}", status_code=status.HTTP_202_ACCEPTED)
async def put_personagem(personagem_id: int, personagem: dict):
    if personagem_id in personagens:
        personagens[personagem_id] = personagem
        return {"id": personagem_id, **personagem}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")


@app.delete("/personagens/{personagem_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_personagem(personagem_id: int):
    if personagem_id in personagens:
        del personagens[personagem_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8002, log_level="info", reload=True)
