# src/features/email_order/router.py

from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.features.email_order.crud import list_email_order
from src.features.email_order.model import EmailOrder  
from src.db import get_session

router = APIRouter(prefix="/threads/{thread_id}/order", tags=["email_order"])

@router.get("/", response_model=list[EmailOrder])
def read_thread_order(thread_id: int, db: Session = Depends(get_session)):
    return list_email_order(db, thread_id)
