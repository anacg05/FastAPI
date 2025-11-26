from fastapi import APIRouter, Form, UploadFile, File, status, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session
from models.files_models import StoredFile
from sqlalchemy.future import select
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.post("/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"Filename": file.filename}

@router.post("/savefile")
async def save_upload_file(file: UploadFile = File(...)):
    with open(f'api/v1/endpoints/uploads/{file.filename}', "wb") as f:
        f.write(file.file.read())
        return{"message": f"File '{file.filename}' saved successfully"}

@router.post("/multiplefiles")
async def multiple_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}

@router.post("/upload_db")
async def upload_file_to_db(file: UploadFile = File(...), db: AsyncSession = Depends(get_session)):
    try:
        content = await file.read()
        novo_file = StoredFile(
            filename = file.filename,
            content_type = file.content_type,
            content = content
        )
        
        db.add(novo_file)
        await db.commit()
        await db.refresh(novo_file)
        return {
            "id": novo_file.id,
            "filename": novo_file.filename,
            "content_type": novo_file.content_type
        }
        
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(e))

@router.get("/download/{file_id}")
async def download_file(file_id: int, db: AsyncSession = Depends(get_session)):
    try:
        query = select(StoredFile).filter(StoredFile.id == file_id)
        result = await db.execute(query)
        stored_file = result.scalar_one_or_none()

        if not stored_file:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Arquivo não encontrado")

        async def file_iterator(data: bytes):
            yield data
            
        return StreamingResponse(
            file_iterator(stored_file.content),
            media_type = stored_file.content_type,
            headers = {
                "Content-Disposition": f"attachment; filename = {stored_file.filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro as fazer dowload: {e}")
