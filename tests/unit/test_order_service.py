import pytest
from src.app.services.order_service import calculate_totals, pay_transition, InvalidOrderError, OrderConflictError

def test_calculate_totals_no_discount():
    items = [{"sku":"A","qty":2,"unit_price":50000}]
    subtotal, discount, total = calculate_totals(items, None)
    assert subtotal == 100000
    assert discount == 0
    assert total == 100000

def test_calculate_totals_off10_with_cap():
    items = [{"sku":"A","qty":200,"unit_price":10000}]
    subtotal, discount, total = calculate_totals(items, "OFF10")
    assert subtotal == 2000000
    assert discount == 100000
    assert total == 1900000

def test_calculate_totals_invalid_qty():
    items = [{"sku":"A","qty":0,"unit_price":100}]
    with pytest.raises(InvalidOrderError):
        calculate_totals(items, None)

def test_pay_transition_created_to_paid():
    assert pay_transition("CREATED") == "PAID"

def test_pay_transition_paid_conflict():
    with pytest.raises(OrderConflictError):
        pay_transition("PAID")
