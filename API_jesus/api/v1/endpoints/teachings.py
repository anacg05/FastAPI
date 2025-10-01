from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.db import get_db
from models.teaching import Teaching
from schemas.teaching import TeachingCreate, TeachingUpdate, TeachingOut

router = APIRouter(prefix="/teachings", tags=["teachings"])

# Listar teachings com paginação e busca
@router.get("/", response_model=dict)
def list_teachings(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), q: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Teaching)
    if q:
        like = f"%{q}%"
        query = query.filter(Teaching.title.ilike(like) | Teaching.content.ilike(like))
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    total = query.count()
    return {"data": items, "meta": {"page": page, "page_size": page_size, "total": total}}

# Criar novo teaching
@router.post("/", response_model=TeachingOut, status_code=201)
def create_teaching(payload: TeachingCreate, db: Session = Depends(get_db)):
    obj = Teaching(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# Obter um teaching específico
@router.get("/{teaching_id}", response_model=TeachingOut)
def get_teaching(teaching_id: int, db: Session = Depends(get_db)):
    obj = db.query(Teaching).get(teaching_id)
    if not obj:
        raise HTTPException(404, "Not found")
    return obj

# Atualizar teaching
@router.patch("/{teaching_id}", response_model=TeachingOut)
def update_teaching(teaching_id: int, payload: TeachingUpdate, db: Session = Depends(get_db)):
    obj = db.query(Teaching).get(teaching_id)
    if not obj:
        raise HTTPException(404, "Not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

# Deletar teaching
@router.delete("/{teaching_id}", status_code=204)
def delete_teaching(teaching_id: int, db: Session = Depends(get_db)):
    obj = db.query(Teaching).get(teaching_id)
    if not obj:
        raise HTTPException(404, "Not found")
    db.delete(obj)
    db.commit()
