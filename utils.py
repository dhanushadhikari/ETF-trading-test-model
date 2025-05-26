def simulate_growth(initial_capital, monthly_return_percent, months=24):
    capital = [initial_capital]
    for _ in range(months):
        capital.append(capital[-1] * (1 + monthly_return_percent / 100))
    return capital
