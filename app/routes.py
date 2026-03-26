from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import get_db

router = APIRouter()


@router.get("/banks", response_model=List[schemas.BankOut])
def list_banks(db: Session = Depends(get_db)):
    banks = db.query(models.Bank).all()
    return banks


@router.get("/branches", response_model=schemas.BranchOut)
def get_branch(ifsc: str, db: Session = Depends(get_db)):
    branch = db.query(models.Branch).filter(models.Branch.ifsc == ifsc).first()
    if not branch:
        raise HTTPException(status_code=404, detail="IFSC not found")
    return branch
