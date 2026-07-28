# Regras de fraude

As regras atuais são:

- `high_amount`: valor acima do limite configurado.
- `profile_amount_mismatch`: valor incompatível com perfil sintético.
- `risky_location`: estado presente na lista educacional de risco.
- `burst_transactions`: múltiplas transações do mesmo cliente sintético em janela curta.
- `device_change`: dispositivo diferente do usual.
- `unusual_hour`: horário incomum.
- `combined_risk_signals`: combinação de valor, localização e mudança de estado.

Cada regra tem identificador, descrição, peso e evidências. A pontuação é limitada a 100 e classificada como `low`, `medium` ou `high`.

Limitação: regras estáticas podem gerar falsos positivos e falsos negativos. Um modelo de ML futuro poderia consumir o mesmo contrato de dados e devolver uma pontuação probabilística, mantendo as regras como camada explicável.
