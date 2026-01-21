terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  # Trava a versão do Terraform para evitar quebras futuras
  required_version = ">= 1.0.0"
}

provider "aws" {
  region = "us-east-1"

  # Prática de FinOps: Tagueamento automático de todos os recursos
  default_tags {
    tags = {
      Project     = "FraudDetection"
      Environment = "Dev"
      ManagedBy   = "Terraform"
      Owner       = "Thiago"
    }
  }
}