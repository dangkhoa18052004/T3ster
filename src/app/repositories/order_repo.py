from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models import Order, OrderItem, User

class OrderRepo:
    def __init__(self, db: Session):
        self.db = db

    def user_exists(self, user_id: str) -> bool:
        stmt = select(User.id).where(User.id == user_id)
        return self.db.execute(stmt).first() is not None

    def create_order_with_items(self, user_id: str, status: str, subtotal: int, discount: int, total: int, items: list[dict]) -> Order:
        order = Order(user_id=user_id, status=status, subtotal=subtotal, discount=discount, total=total)
        self.db.add(order)
        self.db.flush()

        for it in items:
            qty = int(it["qty"])
            unit_price = int(it["unit_price"])
            line_total = qty * unit_price
            oi = OrderItem(order_id=order.id, sku=it["sku"], qty=qty, unit_price=unit_price, line_total=line_total)
            self.db.add(oi)

        self.db.commit()
        self.db.refresh(order)
        return order

    def get_order(self, order_id: str) -> Order | None:
        return self.db.get(Order, order_id)

    def list_items(self, order_id: str) -> list[OrderItem]:
        stmt = select(OrderItem).where(OrderItem.order_id == order_id)
        return [row[0] for row in self.db.execute(stmt).all()]

    def update_status(self, order: Order, new_status: str) -> Order:
        order.status = new_status
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order
