from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, deps
from datetime import datetime
from typing import Optional
from fastapi import Query

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("/", response_model=list[schemas.TransactionWithCategory])
def get_transactions(
    type: Optional[str] = Query(None),  # 'income' or 'expense'
    startDate: Optional[str] = Query(None),
    endDate: Optional[str] = Query(None),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)  # User 객체 받기
):
    query = db.query(models.Transaction).join(models.Category).filter(models.Transaction.user_id == current_user.id)

    if type:
        query = query.filter(models.Category.type == type)
    if startDate:
        start_dt = datetime.fromisoformat(startDate)
        query = query.filter(models.Transaction.transaction_date >= start_dt)
    if endDate:
        end_dt = datetime.fromisoformat(endDate)
        query = query.filter(models.Transaction.transaction_date <= end_dt)

    return query.all()

@router.post("/", response_model=schemas.TransactionWithCategory)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    db_transaction = models.Transaction(
        user_id=current_user.id,
        category_id=transaction.category_id,
        amount=transaction.amount,
        description=transaction.description,
        transaction_date=transaction.transaction_date  # ✅ 그냥 그대로 사용
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction
