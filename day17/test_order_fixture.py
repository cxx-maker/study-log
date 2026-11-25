import pytest
from db import query, execute


@pytest.fixture
def one_order():
    execute("INSERT INTO orders (user_id, amount, created_at) VALUES (1, 10.00, '2026-03-01')")
    yield
    execute("DELETE FROM orders WHERE amount = 10.00")


def test_orders_count(one_order):
    rows = query("SELECT COUNT(*) AS c FROM orders")
    assert rows[0]["c"] == 13
