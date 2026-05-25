import random


def generate_chargers(quantity: int) -> list[dict]:
    """Gera carregadores e sessões de recarga simuladas."""
    chargers = []

    for index in range(1, quantity + 1):
        status = random.choices(
            ["charging", "waiting", "available"],
            weights=[0.65, 0.20, 0.15],
            k=1
        )[0]

        requested_kw = 0 if status == "available" else random.choice([7.4, 11, 22, 30])
        energy_kwh = 0 if status == "available" else round(random.uniform(5, 48), 2)

        chargers.append({
            "charger_id": f"CP-{index:02d}",
            "vehicle_id": "-" if status == "available" else f"EV-{random.randint(100, 999)}",
            "status": status,
            "requested_kw": float(requested_kw),
            "delivered_kw": 0.0,
            "energy_kwh": energy_kwh,
            "start_hour": random.randint(0, 23),
            "priority": random.choice(["normal", "alta", "baixa"])
        })

    return chargers


def generate_historical_demand() -> list[float]:
    """Retorna uma série simples de demanda histórica em kW."""
    return [42, 48, 55, 61, 74, 88, 92, 80, 67, 58, 63, 71]
