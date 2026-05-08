from app.jobs.dead_stock import calculate_discounted_price


def test_discount_calculation():
    assert calculate_discounted_price(1000, 10) == 900
    assert calculate_discounted_price(500, 20) == 400