# Estimativa de custos

Custos dependem de região, volume e retenção. Principais fontes:

- Amazon S3: armazenamento, requisições e transferência.
- Amazon Athena: dados escaneados por consulta.
- AWS Glue Data Catalog: metadados.
- Amazon CloudWatch Logs: ingestão e retenção.
- Amazon Kinesis Data Streams: custo recorrente por shard quando `enable_streaming = true`.

Para manter baixo custo, use poucos eventos, Parquet particionado, retenção curta de logs e streaming desligado quando não estiver estudando esse modo.
