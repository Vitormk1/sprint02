def balance_power(chargers: list[dict], max_power_kw: float) -> list[dict]:
    """
    Distribui a potência disponível entre os carregadores ativos.

    Regra usada na prova de conceito:
    - carregadores disponíveis recebem 0 kW;
    - carregadores com prioridade alta recebem peso maior;
    - se a demanda total for menor que o limite, todos recebem o solicitado;
    - se a demanda total ultrapassar o limite, a potência é rateada por peso.
    """
    active = [c for c in chargers if c["status"] in ["charging", "waiting"]]
    total_requested = sum(c["requested_kw"] for c in active)

    if total_requested <= max_power_kw:
        for charger in chargers:
            charger["delivered_kw"] = charger["requested_kw"]
        return chargers

    priority_weight = {
        "alta": 1.4,
        "normal": 1.0,
        "baixa": 0.7
    }

    weighted_demand = sum(
        c["requested_kw"] * priority_weight.get(c["priority"], 1.0)
        for c in active
    )

    for charger in chargers:
        if charger["status"] == "available":
            charger["delivered_kw"] = 0.0
            continue

        weight = priority_weight.get(charger["priority"], 1.0)
        proportional_power = (
            charger["requested_kw"] * weight / weighted_demand
        ) * max_power_kw

        charger["delivered_kw"] = round(
            min(charger["requested_kw"], proportional_power),
            2
        )

    return chargers
