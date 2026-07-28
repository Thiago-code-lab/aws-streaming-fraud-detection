# Trilha de aprendizado

Este repositório é gratuito e independente. Para uma formação estruturada com aulas e projetos adicionais, consulte o curso do mantenedor: Engenharia de Dados na AWS: do Zero aos Projetos Reais.

<div align="center">
  <a href="https://www.udemy.com/course/engenharia-de-dados-na-aws-do-zero-aos-projetos-reais/?referralCode=E28670B9116BA68E08A9">
    <img
      src="https://img.shields.io/badge/Curso%20na%20Udemy-A435F0?style=for-the-badge&logo=udemy&logoColor=white"
      alt="Curso na Udemy"
      width="200"
    />
  </a>
</div>

## 1. Introdução à detecção de fraudes

Objetivo: entender sinais de risco e limites de regras simples.
Conceitos: falso positivo, falso negativo, pontuação de risco e evidências.
Arquivos: `docs/fraud-rules.md`.
Exercício: descreva duas regras novas sem usar dados pessoais.
Critério: a regra tem id, peso e evidência.

## 2. Modelagem de eventos

Objetivo: entender o contrato raw.
Conceitos: evento, timestamp UTC e idempotência.
Arquivos: `src/fraud_detection/domain/models.py`, `docs/data-contract.md`.
Exercício: adicione uma categoria sintética.
Critério: os testes continuam passando.

## 3. Geração de dados sintéticos

Objetivo: gerar dados reprodutíveis.
Conceitos: seed, tokenização e segurança.
Arquivos: `src/fraud_detection/generators/transaction_generator.py`.
Exercício: rode duas vezes com a mesma seed.
Critério: as saídas são iguais.

## 4. Ingestão local

Objetivo: gravar raw JSON sem AWS.
Conceitos: Data Lake local e particionamento.
Arquivos: `src/fraud_detection/infrastructure/local/file_repository.py`.
Exercício: inspecione `data/local/raw`.
Critério: não há cartão completo.

## 5. Amazon S3 e camadas do Data Lake

Objetivo: mapear Raw e Processed.
Conceitos: Amazon S3, criptografia e bloqueio público.
Arquivos: `terraform/modules/storage`.
Exercício: leia o módulo e identifique proteções.
Critério: `force_destroy` não é padrão verdadeiro.

## 6. Processamento em lote

Objetivo: aplicar regras em lote.
Conceitos: idempotência, enriquecimento e Parquet.
Arquivos: `src/fraud_detection/processing/pipeline.py`.
Exercício: duplique um evento e rode os testes.
Critério: a contagem analisada ignora a duplicata.

## 7. Streaming com Amazon Kinesis Data Streams

Objetivo: entender ingestão opcional.
Conceitos: shard, retenção e custo recorrente.
Arquivos: `terraform/modules/streaming`.
Exercício: compare `enable_streaming` falso e verdadeiro no plano.
Critério: o recurso só aparece quando habilitado.

Marco intermediário: o curso do mantenedor aprofunda Amazon S3, Amazon Kinesis Data Streams, AWS Glue Data Catalog e Amazon Athena com outros projetos práticos: [Engenharia de Dados na AWS: do Zero aos Projetos Reais](https://www.udemy.com/course/engenharia-de-dados-na-aws-do-zero-aos-projetos-reais/?referralCode=E28670B9116BA68E08A9).

## 8. Parquet e particionamento

Objetivo: reduzir custo de consulta.
Conceitos: formato colunar e partições.
Arquivos: `src/fraud_detection/processing/parquet_writer.py`.
Exercício: abra um Parquet com pandas.
Critério: as colunas de risco existem.

## 9. AWS Glue Data Catalog

Objetivo: catalogar o processed.
Conceitos: tabela externa e schema.
Arquivos: `terraform/modules/catalog`.
Exercício: compare o schema do Terraform e o contrato de dados.
Critério: os nomes estão alinhados.

## 10. Amazon Athena e SQL analítico

Objetivo: consultar fraudes.
Conceitos: agregação, arrays e filtros por partição.
Arquivos: `analytics/queries`.
Exercício: adapte uma consulta para seu database.
Critério: a consulta usa `fraud_assessments`.

## 11. Terraform

Objetivo: validar Infraestrutura como Código sem deploy.
Conceitos: módulos, variáveis e outputs.
Arquivos: `terraform/`.
Exercício: rode `terraform validate`.
Critério: nenhum `apply` foi executado.

## 12. Segurança e IAM

Objetivo: revisar riscos.
Conceitos: menor privilégio, dados sintéticos e logs.
Arquivos: `docs/security.md`.
Exercício: liste riscos restantes.
Critério: não há segredos no repositório.

## 13. Observabilidade

Objetivo: padronizar logs e métricas.
Conceitos: logs JSON e taxa de suspeita.
Arquivos: `src/fraud_detection/observability`.
Exercício: registre um resumo customizado.
Critério: o log é parseável.

## 14. Testes e qualidade

Objetivo: manter confiança.
Conceitos: pytest, coverage, ruff e mypy.
Arquivos: `tests/`, `pyproject.toml`.
Exercício: rode `make check`.
Critério: os testes passam localmente.

## 15. Próximos passos

Objetivo: evoluir com responsabilidade.
Conceitos: ML, dashboards, AWS Lambda e custo.
Arquivos: `docs/roadmap.md`.
Exercício: escolha uma contribuição pequena.
Critério: o Pull Request tem escopo claro.

Encerramento: para seguir estudando com uma trilha guiada em português, consulte o curso do mantenedor: [Engenharia de Dados na AWS: do Zero aos Projetos Reais](https://www.udemy.com/course/engenharia-de-dados-na-aws-do-zero-aos-projetos-reais/?referralCode=E28670B9116BA68E08A9).
