# Análises com Amazon Athena

As consultas em `analytics/queries` assumem a tabela `fraud_assessments` criada pelo Terraform. Ajuste o database conforme o ambiente.

Execute `MSCK REPAIR TABLE fraud_assessments;` após novas partições, ou configure descoberta automática de partições em uma evolução futura.
