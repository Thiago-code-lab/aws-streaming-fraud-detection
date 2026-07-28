# Arquitetura

O projeto possui dois modos: local e AWS. O modo local é o caminho recomendado para estudo inicial porque não exige credenciais nem cria recursos.

```mermaid
flowchart LR
  Generator[Gerador sintético] --> Validator[Validador de schema]
  Validator --> Raw[Raw JSON]
  Raw --> Rules[Motor de regras]
  Rules --> Score[Pontuação, nível e evidências]
  Score --> Processed[Processed JSON]
  Score --> Parquet[Parquet particionado]
  Parquet --> Athena[Amazon Athena via AWS Glue]
  Generator -. opcional .-> Kinesis[Amazon Kinesis Data Streams]
  Kinesis -.-> Consumer[Consumidor]
  Consumer -.-> Raw
```

As regras são educacionais e explicáveis. Elas não substituem modelos antifraude reais.
