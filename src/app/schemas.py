from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

class UserCreate(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    full_name: str = Field(min_length=1, max_length=255)

class UserOut(BaseModel):
    id: str
    email: str
    full_name: str
    created_at: datetime

class OrderItemIn(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    qty: int = Field(gt=0)
    unit_price: int = Field(ge=0)

class OrderCreate(BaseModel):
    user_id: str
    discount_code: Optional[str] = None
    items: List[OrderItemIn] = Field(min_length=1)

class OrderItemOut(BaseModel):
    sku: str
    qty: int
    unit_price: int
    line_total: int

class OrderOut(BaseModel):
    id: str
    user_id: str
    status: str
    subtotal: int
    discount: int
    total: int
    created_at: datetime
    items: list[OrderItemOut]
