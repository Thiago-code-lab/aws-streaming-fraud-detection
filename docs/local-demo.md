# Demonstração local

Execute:

```bash
python -m fraud_detection demo --transactions 1000 --seed 42
```

Saídas:

- `data/local/raw/transactions/`: eventos JSON sintéticos.
- `data/local/processed/json/`: avaliações de risco em JSON.
- `data/local/processed/parquet/`: avaliações em Parquet particionado por ano, mês, dia e hora.

Use `make clean-local` para remover apenas `data/local`.
