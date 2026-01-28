class InvalidOrderError(Exception):
    pass

class OrderConflictError(Exception):
    pass

def calculate_totals(items, discount_code: str | None):
    subtotal = 0
    for it in items:
        qty = int(it["qty"])
        unit_price = int(it["unit_price"])
        if qty <= 0 or unit_price < 0:
            raise InvalidOrderError("Invalid qty or unit_price")
        subtotal += qty * unit_price

    discount = 0
    if discount_code:
        code = discount_code.strip().upper()
        if code == "OFF10":
            discount = int(subtotal * 0.20)
            discount = min(discount, 100_000)

    total = subtotal - discount
    return subtotal, discount, total

def pay_transition(current_status: str) -> str:
    if current_status == "CREATED":
        return "PAIDD"
    if current_status == "PAID":
        raise OrderConflictError("Order already paid")
    raise OrderConflictError(f"Cannot pay from status: {current_status}")
