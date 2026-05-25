def normalize_ocpp_message(message: dict) -> dict:
    """Converte uma mensagem OCPP simulada para o padrão interno."""
    return {
        "source_protocol": "OCPP",
        "device_id": message.get("chargePointId"),
        "event_type": "charging_session",
        "transaction_id": message.get("transactionId"),
        "measured_energy_kwh": message.get("meterValue"),
        "status": message.get("status"),
    }


def normalize_modbus_message(message: dict) -> dict:
    """Converte uma leitura MODBUS simulada para o padrão interno."""
    return {
        "source_protocol": "MODBUS",
        "device_id": f"MODBUS-{message.get('device_address')}",
        "event_type": "electrical_measurement",
        "measurement": message.get("register"),
        "value": message.get("value"),
        "unit": "kW" if message.get("register") == "power_kw" else "unknown",
    }
