def is_peak_hour(hour: int) -> bool:
    """Define horário de pico para a simulação."""
    return 18 <= hour <= 21


def calculate_session_cost(
    energy_kwh: float,
    hour: int,
    demand_ratio: float,
    base_price: float,
    peak_multiplier: float
) -> float:
    """
    Calcula custo estimado da sessão.

    Fórmula simplificada:
    custo = energia * tarifa_base * fator_horario * fator_demanda
    """
    time_factor = peak_multiplier if is_peak_hour(hour) else 1.0

    if demand_ratio >= 0.90:
        demand_factor = 1.25
    elif demand_ratio >= 0.70:
        demand_factor = 1.10
    else:
        demand_factor = 1.0

    return round(energy_kwh * base_price * time_factor * demand_factor, 2)
