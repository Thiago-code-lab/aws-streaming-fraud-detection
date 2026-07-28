# Deploy na AWS

O projeto não executa deploy automaticamente. Revise o plano antes de aplicar.

```bash
cd terraform/environments/dev
cp terraform.tfvars.example terraform.tfvars
terraform init -backend=false
terraform plan
```

Configure `unique_suffix` com um valor não secreto. O processamento em streaming fica desligado por padrão com `enable_streaming = false`.

Para destruir, use `terraform destroy` somente no ambiente que você criou e depois de revisar buckets, custos e dados.
