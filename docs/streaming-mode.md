# Processamento em streaming

O processamento em streaming usa Amazon Kinesis Data Streams de forma opcional. Ele existe para demonstrar ingestão contínua, mas gera custo recorrente mesmo em baixo volume.

Habilite apenas quando necessário:

```hcl
enable_streaming = true
kinesis_shard_count = 1
```

O produtor `KinesisProducer` publica eventos validados. Um consumidor AWS Lambda pode usar `parse_kinesis_records` para transformar registros em `Transaction`.
