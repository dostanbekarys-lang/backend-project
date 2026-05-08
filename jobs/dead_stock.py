def calculate_discounted_price(price: float, discount_percent: float) -> float:
    return round(price * (1 - discount_percent / 100), 2)