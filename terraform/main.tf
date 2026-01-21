# --- Data Lake (Armazenamento) ---

# Bucket para dados brutos (Raw)
resource "aws_s3_bucket" "raw_bucket" {
  bucket_prefix = "fraud-detection-raw-" # Garante nome único global
  force_destroy = true                   # PERMITE DELETAR MESMO COM ARQUIVOS
}

# Bucket para dados tratados (Processed)
resource "aws_s3_bucket" "processed_bucket" {
  bucket_prefix = "fraud-detection-processed-"
  force_destroy = true
}

# Bloqueio de Acesso Público (Segurança Padrão DevSecOps)
resource "aws_s3_bucket_public_access_block" "raw_block" {
  bucket = aws_s3_bucket.raw_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "processed_block" {
  bucket = aws_s3_bucket.processed_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}


# --- Ingestão (Streaming) ---
# BLOQUEADO TEMPORARIAMENTE (Aguardando liberação da AWS)
/*
resource "aws_kinesis_stream" "transaction_stream" {
  name             = "fraud-detection-stream"
  shard_count      = 1             # CUSTO MÍNIMO: Apenas 1 shard (~$0.015/hora)
  retention_period = 24            # Mínimo de 24 horas para economizar armazenamento
  
  # Modo provisionado é mais barato para testes contínuos de baixo volume
  stream_mode_details {
    stream_mode = "PROVISIONED"
  }

  tags = {
    Name = "TransactionStream"
  }
}
*/