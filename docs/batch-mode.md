# Processamento em lote

O modo de processamento em lote preserva a ideia original do projeto:

1. Eventos JSON chegam ao S3 Raw.
2. O pipeline valida e aplica regras.
3. Avaliações são gravadas no S3 Processed em Parquet.
4. O AWS Glue Data Catalog cataloga a tabela.
5. O Amazon Athena consulta os dados.

Os nomes dos buckets devem vir de outputs do Terraform ou variáveis de ambiente, nunca de hardcode no código Python.
