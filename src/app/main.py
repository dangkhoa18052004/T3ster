from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .schemas import UserCreate, UserOut, OrderCreate, OrderOut
from .repositories.user_repo import UserRepo
from .repositories.order_repo import OrderRepo
from .services.user_service import ensure_email_unique, DuplicateEmailError
from .services.order_service import calculate_totals, pay_transition, InvalidOrderError, OrderConflictError

app = FastAPI(title="Order API (CI Demo)")

# Demo-friendly: auto-create tables (production would use Alembic migrations)
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/users", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepo(db)
    try:
        email = ensure_email_unique(payload.email, repo)
    except DuplicateEmailError:
        raise HTTPException(status_code=409, detail="Email already exists")

    try:
        u = repo.create(email=email, full_name=payload.full_name)
        return u
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: str, db: Session = Depends(get_db)):
    repo = UserRepo(db)
    u = repo.get(user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u

@app.post("/orders", response_model=OrderOut, status_code=201)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    orepo = OrderRepo(db)
    if not orepo.user_exists(payload.user_id):
        raise HTTPException(status_code=404, detail="User not found")

    try:
        items = [it.model_dump() for it in payload.items]
        subtotal, discount, total = calculate_totals(items, payload.discount_code)
    except InvalidOrderError as e:
        raise HTTPException(status_code=422, detail=str(e))

    order = orepo.create_order_with_items(
        user_id=payload.user_id,
        status="CREATED",
        subtotal=subtotal,
        discount=discount,
        total=total,
        items=items,
    )
    db_items = orepo.list_items(order.id)
    return {
        "id": order.id,
        "user_id": order.user_id,
        "status": order.status,
        "subtotal": order.subtotal,
        "discount": order.discount,
        "total": order.total,
        "created_at": order.created_at,
        "items": [
            {"sku": i.sku, "qty": i.qty, "unit_price": i.unit_price, "line_total": i.line_total}
            for i in db_items
        ],
    }

@app.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: str, db: Session = Depends(get_db)):
    orepo = OrderRepo(db)
    order = orepo.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    items = orepo.list_items(order.id)
    return {
        "id": order.id,
        "user_id": order.user_id,
        "status": order.status,
        "subtotal": order.subtotal,
        "discount": order.discount,
        "total": order.total,
        "created_at": order.created_at,
        "items": [
            {"sku": i.sku, "qty": i.qty, "unit_price": i.unit_price, "line_total": i.line_total}
            for i in items
        ],
    }

@app.post("/orders/{order_id}/pay")
def pay_order(order_id: str, db: Session = Depends(get_db)):
    orepo = OrderRepo(db)
    order = orepo.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    try:
        new_status = pay_transition(order.status)
    except OrderConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))

    orepo.update_status(order, new_status)
    return {"id": order.id, "status": order.status}
