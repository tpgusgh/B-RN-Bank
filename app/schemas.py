from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime

# User
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True

# Category
class CategoryBase(BaseModel):
    name: str
    type: Literal["income", "expense"]
    color: Optional[str] = "#3B82F6"

class CategoryCreate(BaseModel):
    name: str
    type: str
    color: str

class Category(CategoryBase):
    id: str
    user_id: str
    created_at: datetime
    class Config:
        orm_mode = True

# Transaction
class TransactionBase(BaseModel):
    category_id: Optional[str]
    amount: float
    description: Optional[str] = ""
    transaction_date: datetime


class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: str
    user_id: str
    created_at: datetime
    class Config:
        orm_mode = True

class TransactionWithCategory(Transaction):
    category: Optional[Category]


class TransactionStat(BaseModel):
    transaction_id: str
    category_id: int
    category_name: str
    category_color: str
    amount: float
    transaction_date: datetime