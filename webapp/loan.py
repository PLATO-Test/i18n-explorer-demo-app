def monthly_payment(amount: float, term_months: int, annual_rate: float) -> float:
    monthly_rate = annual_rate / 12
    if monthly_rate == 0:
        return round(amount / term_months, 2)
    factor = (1 + monthly_rate) ** term_months
    payment = amount * monthly_rate * factor / (factor - 1)
    return round(payment, 2)
