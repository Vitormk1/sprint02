import streamlit as st
import pandas as pd
import plotly.express as px

from src.simulator import generate_chargers, generate_historical_demand
from src.demand_manager import balance_power
from src.tariff import calculate_session_cost
from src.protocol_adapter import normalize_ocpp_message, normalize_modbus_message
from src.forecast import moving_average_forecast


st.set_page_config(
    page_title="ChargeGrid Intelligence",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ ChargeGrid Intelligence")
st.caption("Sprint 2 — Prova de Conceito Funcional")

st.markdown(
    """
    Esta interface simula o funcionamento de uma plataforma para gerenciamento inteligente
    de carregadores de veículos elétricos em ambientes comerciais.
    """
)

with st.sidebar:
    st.header("Configuração da simulação")

    total_power = st.slider(
        "Potência máxima disponível no local (kW)",
        min_value=20,
        max_value=200,
        value=80,
        step=5
    )

    charger_count = st.slider(
        "Quantidade de carregadores",
        min_value=2,
        max_value=12,
        value=6,
        step=1
    )

    peak_multiplier = st.slider(
        "Fator de tarifa em horário de pico",
        min_value=1.0,
        max_value=3.0,
        value=1.6,
        step=0.1
    )

    base_price = st.number_input(
        "Tarifa base por kWh (R$)",
        min_value=0.10,
        max_value=5.00,
        value=1.20,
        step=0.05
    )

    st.divider()
    st.caption("Objetivo: evitar sobrecarga e calcular custos de recarga.")

chargers = generate_chargers(charger_count)
balanced = balance_power(chargers, total_power)

df = pd.DataFrame(balanced)

df["cost_estimate"] = df.apply(
    lambda row: calculate_session_cost(
        energy_kwh=row["energy_kwh"],
        hour=row["start_hour"],
        demand_ratio=df["delivered_kw"].sum() / total_power,
        base_price=base_price,
        peak_multiplier=peak_multiplier
    ),
    axis=1
)

total_requested = df["requested_kw"].sum()
total_delivered = df["delivered_kw"].sum()
active_chargers = int(df[df["status"] == "charging"].shape[0])
overload_avoided = max(total_requested - total_power, 0)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Potência solicitada", f"{total_requested:.1f} kW")
col2.metric("Potência entregue", f"{total_delivered:.1f} kW")
col3.metric("Carregadores ativos", active_chargers)
col4.metric("Sobrecarga evitada", f"{overload_avoided:.1f} kW")

st.divider()

left, right = st.columns([1.2, 1])

with left:
    st.subheader("Balanceamento de potência")

    power_chart = px.bar(
        df,
        x="charger_id",
        y=["requested_kw", "delivered_kw"],
        barmode="group",
        labels={
            "value": "Potência (kW)",
            "charger_id": "Carregador",
            "variable": "Tipo"
        },
        title="Potência solicitada x potência entregue"
    )
    st.plotly_chart(power_chart, use_container_width=True)

with right:
    st.subheader("Status operacional")

    status_df = df["status"].value_counts().reset_index()
    status_df.columns = ["status", "quantity"]

    status_chart = px.pie(
        status_df,
        names="status",
        values="quantity",
        title="Distribuição dos carregadores"
    )
    st.plotly_chart(status_chart, use_container_width=True)

st.subheader("Sessões simuladas de recarga")
st.dataframe(
    df[
        [
            "charger_id",
            "vehicle_id",
            "status",
            "requested_kw",
            "delivered_kw",
            "energy_kwh",
            "start_hour",
            "cost_estimate",
            "priority"
        ]
    ],
    use_container_width=True
)

st.divider()

st.subheader("Tarifação dinâmica")

tariff_chart = px.bar(
    df,
    x="charger_id",
    y="cost_estimate",
    labels={
        "cost_estimate": "Custo estimado (R$)",
        "charger_id": "Carregador"
    },
    title="Custo estimado por sessão"
)
st.plotly_chart(tariff_chart, use_container_width=True)

st.divider()

st.subheader("Interoperabilidade: OCPP + MODBUS simulados")

sample_ocpp = {
    "protocol": "OCPP",
    "chargePointId": "CP-01",
    "transactionId": "TX-1001",
    "meterValue": 18.7,
    "status": "Charging"
}

sample_modbus = {
    "protocol": "MODBUS",
    "device_address": 12,
    "register": "power_kw",
    "value": 42.5
}

protocol_left, protocol_right = st.columns(2)

with protocol_left:
    st.markdown("**Mensagem OCPP simulada**")
    st.json(sample_ocpp)
    st.markdown("**Formato interno padronizado**")
    st.json(normalize_ocpp_message(sample_ocpp))

with protocol_right:
    st.markdown("**Mensagem MODBUS simulada**")
    st.json(sample_modbus)
    st.markdown("**Formato interno padronizado**")
    st.json(normalize_modbus_message(sample_modbus))

st.divider()

st.subheader("Previsão simples de demanda")

historical = generate_historical_demand()
forecast = moving_average_forecast(historical, window=4, steps=4)

historical_df = pd.DataFrame({
    "periodo": list(range(1, len(historical) + 1)),
    "demanda_kw": historical,
    "tipo": "Histórico"
})

forecast_df = pd.DataFrame({
    "periodo": list(range(len(historical) + 1, len(historical) + len(forecast) + 1)),
    "demanda_kw": forecast,
    "tipo": "Previsão"
})

demand_df = pd.concat([historical_df, forecast_df], ignore_index=True)

forecast_chart = px.line(
    demand_df,
    x="periodo",
    y="demanda_kw",
    color="tipo",
    markers=True,
    labels={
        "periodo": "Período",
        "demanda_kw": "Demanda (kW)",
        "tipo": "Tipo"
    },
    title="Histórico e previsão de demanda"
)
st.plotly_chart(forecast_chart, use_container_width=True)

st.info(
    "Nesta prova de conceito, a previsão usa média móvel. Em uma versão futura, "
    "o modelo pode ser substituído por algoritmos de IA com dados reais de consumo, "
    "horário, ocupação e comportamento dos usuários."
)
