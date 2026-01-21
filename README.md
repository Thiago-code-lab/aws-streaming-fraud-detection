# AWS Streaming Fraud Detection Pipeline

Projeto de detecção de fraude em tempo real utilizando serviços AWS como Kinesis, S3, Glue e Spark.

## Estrutura do Projeto

```
aws-streaming-fraud-detection/
├── .gitignore               # Ignorar arquivos temporários e sensíveis
├── README.md                # Documentação principal do projeto
├── architecture/            # Diagramas da solução
├── terraform/               # Infraestrutura como Código (IaC)
├── src/                     # Código fonte da aplicação
│   ├── producer/            # Scripts geradores de dados
│   └── processing/          # Jobs Spark/Glue
└── tests/                   # Testes de qualidade de dados
```

## Fases do Projeto

- **Fase 1**: Infraestrutura AWS com Terraform
- **Fase 2**: Scripts geradores de dados de transações
- **Fase 3**: Jobs de processamento e detecção de fraude

## Tecnologias Utilizadas

- AWS Kinesis Data Streams
- AWS S3
- AWS Glue
- Apache Spark
- Python
- Terraform

## Como Usar

1. Configure suas credenciais AWS
2. Execute `terraform init` e `terraform apply` na pasta terraform/
3. Execute os scripts de geração de dados
4. Monitore os resultados nos jobs Glue

## Licença

MIT License
