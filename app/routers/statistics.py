from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from pydantic import BaseModel

from app.database import get_db
from app.models import Transaction, Category, User
from app.deps import get_current_user

router = APIRouter(prefix="/statistics", tags=["statistics"])


class CategoryStats(BaseModel):
    category_id: str
    category_name: str
    category_color: str
    total: float
    count: int
    percentage: float
    descriptions: str = ""  # 기본값 추가
    date: str  # 거래 날짜 추가


class StatisticsResponse(BaseModel):
    totalAmount: float
    categoryStats: List[CategoryStats]


@router.get("/", response_model=StatisticsResponse)
def get_statistics(
    type: str = Query(..., regex="^(income|expense)$"),
    startDate: str = Query(...),
    endDate: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        start = datetime.strptime(startDate, "%Y-%m-%d")
        end = datetime.strptime(endDate, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    transactions = (
    db.query(
        Transaction.amount,
        Transaction.description,
        Transaction.transaction_date,
        Category.id.label("category_id"),
        Category.name.label("category_name"),
        Category.color.label("category_color"),
    )
    .join(Category, Transaction.category_id == Category.id)
    .filter(
        Transaction.user_id == current_user.id,
        Category.type == type,
        Transaction.transaction_date >= start,
        Transaction.transaction_date <= end
    )
    .all()
)


    total_amount = sum(float(t.amount) for t in transactions)

    category_stats = []
    for t in transactions:
        category_stats.append(
            CategoryStats(
                category_id=str(t.category_id),
                category_name=t.category_name or "Unknown",
                category_color=t.category_color or "#000000",
                total=float(t.amount),
                count=1,
                descriptions = (t.description or ""),
                percentage=round((float(t.amount) / total_amount) * 100, 2) if total_amount > 0 else 0,
                date=t.transaction_date.strftime("%Y-%m-%d")
            )
        )

    return StatisticsResponse(totalAmount=float(total_amount), categoryStats=category_stats)
