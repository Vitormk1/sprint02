# Arquitetura — ChargeGrid Intelligence

## Fluxo lógico

```text
1. Carregadores simulados geram sessões de recarga
2. Dados de carregadores são tratados como mensagens OCPP
3. Dados elétricos são tratados como leituras MODBUS
4. A camada de interoperabilidade normaliza os dados
5. O motor de decisão calcula:
   - demanda total solicitada
   - potência máxima disponível
   - potência entregue para cada carregador
   - custo estimado da sessão
6. O dashboard exibe:
   - potência solicitada
   - potência entregue
   - sobrecarga evitada
   - custos
   - status dos carregadores
   - previsão de demanda
```

## Componentes

### Interface

Arquivo: `app.py`

Responsável por apresentar o dashboard e conectar as regras de negócio.

### Simulador

Arquivo: `src/simulator.py`

Gera sessões de recarga fictícias para representar um ambiente comercial.

### Gerenciador de demanda

Arquivo: `src/demand_manager.py`

Aplica a regra de balanceamento de carga.

### Tarifação

Arquivo: `src/tariff.py`

Calcula o custo estimado de cada sessão.

### Interoperabilidade

Arquivo: `src/protocol_adapter.py`

Simula a conversão de OCPP e MODBUS para um padrão interno.

### Previsão

Arquivo: `src/forecast.py`

Aplica média móvel para prever demanda futura.
