from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, deps
from datetime import datetime
from .. import models, deps, schemas
router = APIRouter(prefix="/categories", tags=["categories"])
from fastapi import HTTPException, status
from pydantic import BaseModel
from uuid import UUID




@router.get("/")
def get_categories(
    type: str,
    startDate: str,
    endDate: str,
    db: Session = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_user),
):
    start_date = datetime.fromisoformat(startDate)
    end_date = datetime.fromisoformat(endDate)

    categories = db.query(models.Category).filter(
        models.Category.user_id == user.id,
        models.Category.type == type
    ).all()

    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == user.id,
        models.Transaction.transaction_date >= start_date,
        models.Transaction.transaction_date <= end_date
    ).all()

    total = 0
    category_stats = []

    for category in categories:
        cat_txns = [t for t in transactions if t.category_id == category.id]
        cat_total = sum(float(t.amount) for t in cat_txns)
        total += cat_total

        category_stats.append({
            "id": category.id,
            "name": category.name,
            "color": category.color,
            "total": cat_total,
            "type": category.type, 
            "count": len(cat_txns)
        })

    for stat in category_stats:
        stat["percentage"] = (stat["total"] / total * 100) if total > 0 else 0

    return {"total": total, "categories": category_stats}

@router.post("/")
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_user),
):
    new_category = models.Category(
        name=category.name,
        type=category.type,
        color=category.color,
        user_id=user.id
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
@router.delete("/{category_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: UUID,  # int → UUID 로 변경
    db: Session = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_user),
):
    category = db.query(models.Category).filter(
        models.Category.id == str(category_id),  # UUID를 문자열로 저장하는 경우
        models.Category.user_id == user.id
    ).first()

    if not category:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")

    # 관련 거래(category_id가 있는 transaction) 카테고리 제거
    transactions = db.query(models.Transaction).filter(
        models.Transaction.category_id == str(category_id),
        models.Transaction.user_id == user.id
    ).all()

    for txn in transactions:
        txn.category_id = None
        db.add(txn)

    db.delete(category)
    db.commit()

    return {"detail": "카테고리가 삭제되었습니다."}