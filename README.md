# ChargeGrid Intelligence — Sprint 2

Prova de conceito funcional para gerenciamento inteligente de estações de recarga de veículos elétricos em ambientes comerciais.

## 1. Descrição da solução

O **ChargeGrid Intelligence** é uma plataforma proposta para administrar múltiplos carregadores de veículos elétricos em locais como empresas, condomínios, shoppings, estacionamentos corporativos e centros comerciais.

Nesta Sprint 2, a proposta evolui de conceito para uma **simulação funcional**, demonstrando:

- gerenciamento inteligente de demanda;
- balanceamento automático de potência entre carregadores;
- tarifação dinâmica por horário, demanda e energia consumida;
- visualização de sessões de recarga;
- simulação de interoperabilidade entre protocolos como OCPP e MODBUS;
- previsão simples de demanda como base para uso de inteligência artificial.

## 2. Evolução em relação à Sprint 1

Na Sprint 1, o projeto apresentou o problema, os pilares técnicos e a proposta conceitual da solução.

Na Sprint 2, o projeto avança para uma prova de conceito executável, com interface em dashboard e regras funcionais para simular o comportamento do sistema em um cenário comercial.

## 3. Funcionalidades demonstradas

### 3.1 Balanceamento dinâmico de carga

O sistema recebe uma potência máxima disponível para o local e redistribui essa potência entre os carregadores ativos.

Exemplo:

- potência total disponível: 60 kW;
- 4 carregadores ativos solicitando 22 kW cada;
- demanda total solicitada: 88 kW;
- o sistema reduz automaticamente a potência entregue para evitar sobrecarga.

### 3.2 Tarifação dinâmica

A tarifa é calculada considerando:

- consumo em kWh;
- horário da recarga;
- nível de demanda da rede;
- fator de pico.

O objetivo é incentivar o uso fora dos horários de maior demanda.

### 3.3 Simulação de interoperabilidade

O projeto simula uma camada de tradução de protocolos:

- carregadores enviam dados como se fossem mensagens OCPP;
- medidores elétricos enviam dados como se fossem leituras MODBUS;
- o sistema converte tudo para um formato interno padronizado.

### 3.4 Previsão de demanda

A simulação utiliza histórico de consumo para estimar a demanda esperada nos próximos períodos. Essa parte representa a base para aplicação futura de modelos de inteligência artificial.

## 4. Arquitetura do sistema

```text
Carregadores EV
     |
     | OCPP simulado
     v
Camada de Interoperabilidade
     |
     | formato interno padronizado
     v
Motor de Decisão
     |--- Balanceamento de carga
     |--- Tarifação dinâmica
     |--- Previsão de demanda
     v
Dashboard / Interface
     |
     v
Usuário visualiza sessões, custos, potência e alertas
```

## 5. Estrutura do repositório

```text
chargegrid-intelligence-sprint2/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── sample_sessions.csv
└── src/
    ├── __init__.py
    ├── simulator.py
    ├── demand_manager.py
    ├── tariff.py
    ├── protocol_adapter.py
    └── forecast.py
```

## 6. Como executar

> Observação: este projeto foi desenvolvido e testado utilizando **Python 3.12**.  
> Recomenda-se usar essa versão para evitar erros na instalação das dependências.

### 6.2 Criar ambiente virtual

No Windows, utilizando Python 3.12:

```bash
py -3.12 -m venv venv
```

No Linux/Mac:

```bash
python3.12 -m venv venv
```

### 6.3 Ativar ambiente virtual

No Windows:

```bash
venv\Scripts\activate
```

Ou, no PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

No Linux/Mac:

```bash
source venv/bin/activate
```

### 6.4 Atualizar ferramentas de instalação

```bash
python -m pip install --upgrade pip setuptools wheel
```

### 6.5 Instalar dependências

```bash
pip install -r requirements.txt
```

### 6.6 Rodar a aplicação

```bash
python -m streamlit run app.py
```

Depois de executar, o terminal exibirá um link local parecido com:

```text
http://localhost:8501
```

Acesse esse endereço no navegador para visualizar o dashboard.

## 7. Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- Plotly
- Simulação de OCPP
- Simulação de MODBUS
- Regras de negócio para balanceamento de carga
- Modelo simples de previsão por média móvel

## 8. Materiais técnicos relevantes

O projeto simula conceitos utilizados em sistemas reais de recarga inteligente, como:

- controle de demanda;
- limitação de potência;
- gerenciamento de sessões;
- cobrança por energia;
- integração entre sistemas;
- tomada de decisão baseada em dados.

## 9. Integrantes

- João Pedro Ferrari — RM573037
- Nickollas Korner — RM569655
- Lucas Santana — RM573197
- Pierre Biason — RM569718
- Vitor Marcarin — RM571873
- Lucca Bracco — RM570175
