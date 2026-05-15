def test_discount_calculation():
    price = 1000
    discount_percent = 10
    new_price = round(price * (1 - discount_percent / 100), 2)

    assert new_price == 900