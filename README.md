# AWS Fraud Detection Pipeline

<div align="center">

![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

<img width="653" height="382" alt="Image" src="https://github.com/user-attachments/assets/7241d016-bf9e-4c3d-8762-18a9f39e1b59" />

**Pipeline de Engenharia de Dados End-to-End para Detecção de Fraudes em Transações Financeiras**

[Arquitetura](#️-arquitetura) • [Começar](#-como-executar) • [Tecnologias](#️-tecnologias) • [Aprendizados](#-aprendizados)

</div>

---

## 📋 Sobre o Projeto

Pipeline de dados serverless construído na AWS utilizando Infraestrutura como Código (IaC) para detecção automatizada de fraudes em transações financeiras. O projeto implementa boas práticas de engenharia de dados com foco em segurança, escalabilidade e otimização de custos.

## 🏗️ Arquitetura

O pipeline segue uma abordagem **ELT (Extract, Load, Transform)** adaptada para processamento em lote:

```
┌─────────────────┐      ┌──────────────┐      ┌─────────────────┐      ┌──────────────┐
│   Producer      │──────▶│   S3 Raw     │──────▶│  ETL Process    │──────▶│ S3 Processed │
│ (Faker + Boto3) │      │   (JSON)     │      │ (Fraud Detector)│      │  (Parquet)   │
└─────────────────┘      └──────────────┘      └─────────────────┘      └──────────────┘
                                                                                  │
                                                                                  ▼
                                                                         ┌──────────────────┐
                                                                         │  Glue Catalog    │
                                                                         │       +          │
                                                                         │  Amazon Athena   │
                                                                         └──────────────────┘
```

### Componentes

| Camada | Componente | Descrição |
|--------|-----------|-----------|
| **Ingestão** | Producer Script | Gera transações sintéticas usando Python (Boto3 + Faker) e salva como JSON no S3 Raw |
| **Armazenamento** | Data Lake S3 | Buckets segregados (`Raw` e `Processed`) com Block Public Access e versionamento |
| **Processamento** | ETL Pipeline | Converte JSON → Parquet, aplica regras de fraude (valor > R$ 5k ou estados suspeitos) e particiona dados |
| **Analytics** | Glue + Athena | Catálogo de metadados e consultas SQL serverless diretamente no Data Lake |

> **💡 Nota Técnica:** Originalmente projetado para Amazon Kinesis (streaming), o pipeline foi adaptado para processamento em lote via S3 devido a restrições de Account Vetting em contas AWS novas — uma prática comum de DevSecOps para contornar limitações de Service Quotas.

---

## 🚀 Como Executar

### Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- [AWS CLI](https://aws.amazon.com/cli/) configurado com credenciais válidas
- [Terraform](https://www.terraform.io/downloads) >= 1.0
- [Python](https://www.python.org/downloads/) >= 3.8
- pip (gerenciador de pacotes Python)

### Passo 1: Provisionar Infraestrutura

```bash
cd terraform
terraform init
terraform apply -auto-approve
```

**O que será criado:**
- 2 Buckets S3 (raw/processed)
- Glue Database e Crawler
- Políticas IAM necessárias

### Passo 2: Gerar Dados (Ingestão)

```bash
python src/producer/main.py
```
<img width="587" height="259" alt="Image" src="https://github.com/user-attachments/assets/4ebeef1d-8917-4871-a172-02c4554845ec" />

### Digite Ctrl + C para pausar o gerador

<img width="546" height="149" alt="Image" src="https://github.com/user-attachments/assets/669016cd-7aa2-4d83-b859-5e319fa8ae28" />

### Bucket gerado no S3

<img width="1354" height="697" alt="Image" src="https://github.com/user-attachments/assets/aa8953fa-6bd3-4321-adff-f3c1ee213489" />

### Deixe o script executar por alguns segundos para gerar massa de dados suficiente para análise.

### Passo 3: Processar Fraudes (ETL)

```bash
python src/processing/fraud_detector.py
```

**Processo executado:**
- Leitura de JSONs do bucket raw
- Aplicação de regras de detecção de fraude
- Conversão para formato Parquet
- Particionamento por data
- Upload para bucket processed

<img width="1135" height="341" alt="Image" src="https://github.com/user-attachments/assets/ce180e1a-cbc8-4162-b676-84b4bfbf79b6" />

### Passo 4: Analisar Resultados

Acesse o **Amazon Athena** no console da AWS e execute:

```sql
SELECT * FROM fraud_detection_db.fraudes_detectadas;
```

<img width="1000" height="1000" alt="Image" src="https://github.com/user-attachments/assets/f145afdb-1ac3-48e1-acab-4aa6f77c4be3" />

---

## 🛠️ Tecnologias

### Infraestrutura e Cloud
- **Terraform** - Infraestrutura como Código (IaC)
- **AWS S3** - Data Lake (armazenamento Raw e Processed)
- **AWS Glue** - Data Catalog para gerenciamento de metadados
- **Amazon Athena** - Query engine SQL serverless

### Desenvolvimento
- **Python 3.x** - Linguagem principal
- **Boto3** - SDK AWS para Python
- **Pandas** - Manipulação de dados
- **PyArrow** - Suporte a formato Parquet
- **Faker** - Geração de dados sintéticos

### Formatos de Dados
- **JSON** - Formato raw (ingestão)
- **Parquet** - Formato otimizado (processado)

---

## 📌 Aprendizados

Durante o desenvolvimento deste projeto, foram adquiridos conhecimentos sobre:

### Engenharia de Dados
- Implementação de pipeline ELT end-to-end em arquitetura serverless
- Otimização de custos através de formatos colunares (Parquet vs JSON)
- Estratégias de particionamento de dados para performance em queries analíticas

### AWS & DevOps
- Contorno de limitações de Service Quotas em contas AWS novas
- Configuração de políticas de segurança seguindo o princípio de Least Privilege
- Automação de infraestrutura com Terraform (state management, módulos reutilizáveis)

### Boas Práticas
- Segregação de ambientes (Raw/Processed/Analytics)
- Versionamento de dados e controle de acesso granular
- Documentação como código (README técnico estruturado)

---

<div align="center">

**Desenvolvido com foco em boas práticas de Engenharia de Dados e Cloud Architecture**

⭐ Se este projeto foi útil, considere dar uma estrela!

</div>
