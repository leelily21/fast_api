from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal
from app import crud, schemas

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/notes", response_model=schemas.NoteOut)
async def create_note(note: schemas.NoteCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_note(db, note)

@router.get("/notes", response_model=list[schemas.NoteOut])
async def read_notes(db: AsyncSession = Depends(get_db)):
    return await crud.get_notes(db)
