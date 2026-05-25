def moving_average_forecast(values: list[float], window: int = 4, steps: int = 4) -> list[float]:
    """
    Gera previsão simples por média móvel.

    Essa função representa a camada inicial de inteligência do sistema.
    Em uma versão futura, pode ser substituída por um modelo de IA treinado.
    """
    if not values:
        return []

    series = list(values)
    predictions = []

    for _ in range(steps):
        last_values = series[-window:]
        prediction = round(sum(last_values) / len(last_values), 2)
        predictions.append(prediction)
        series.append(prediction)

    return predictions
