from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.db import get_db
from models.parable import Parable
from schemas.parable import ParableCreate, ParableUpdate, ParableOut

router = APIRouter(prefix="/parables", tags=["parables"])

# Listar parables com paginação e busca
@router.get("/", response_model=dict)
def list_parables(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), q: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Parable)
    if q:
        like = f"%{q}%"
        query = query.filter(Parable.title.ilike(like) | Parable.summary.ilike(like))
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    total = query.count()
    return {"data": items, "meta": {"page": page, "page_size": page_size, "total": total}}

# Criar nova parable
@router.post("/", response_model=ParableOut, status_code=201)
def create_parable(payload: ParableCreate, db: Session = Depends(get_db)):
    obj = Parable(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# Obter uma parable específica
@router.get("/{parable_id}", response_model=ParableOut)
def get_parable(parable_id: int, db: Session = Depends(get_db)):
    obj = db.query(Parable).get(parable_id)
    if not obj:
        raise HTTPException(404, "Not found")
    return obj

# Atualizar parable
@router.patch("/{parable_id}", response_model=ParableOut)
def update_parable(parable_id: int, payload: ParableUpdate, db: Session = Depends(get_db)):
    obj = db.query(Parable).get(parable_id)
    if not obj:
        raise HTTPException(404, "Not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

# Deletar parable
@router.delete("/{parable_id}", status_code=204)
def delete_parable(parable_id: int, db: Session = Depends(get_db)):
    obj = db.query(Parable).get(parable_id)
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj)
    db.commit()
