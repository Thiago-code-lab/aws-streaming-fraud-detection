# Contrato de dados

Evento raw:

| Campo | Tipo | Descrição |
| --- | --- | --- |
| transaction_id | string | Identificador idempotente da transação |
| event_timestamp | timestamp UTC | Horário do evento |
| amount | double | Valor sintético |
| state | string | UF |
| device_type | string | `mobile`, `desktop` ou `pos` |
| customer_id | string | Identificador sintético |
| customer_profile_amount | double | Valor médio sintético do perfil |
| customer_home_state | string | UF usual |
| customer_usual_device_type | string | Dispositivo usual |
| masked_card | string | Token mascarado, sem número completo |
| merchant_category | string | Categoria sintética |

Assessment processed adiciona `processed_at`, `risk_score`, `risk_level`, `triggered_rules`, `rule_evidence` e `rules_version`.
