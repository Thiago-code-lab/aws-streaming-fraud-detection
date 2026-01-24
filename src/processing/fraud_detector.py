import boto3
import pandas as pd
import io
from datetime import datetime

# --- CONFIGURAÇÃO ---
SOURCE_BUCKET = "fraud-detection-raw-20260121180915898300000002"
TARGET_BUCKET = "fraud-detection-processed-20260121180915898300000001"

s3_client = boto3.client('s3')

def get_files_from_s3(bucket):
    """Lista todos os arquivos JSON no bucket de origem"""
    print(f"🔍 Listando arquivos em: {bucket}...")
    files = []
    paginator = s3_client.get_paginator('list_objects_v2')
    
    for page in paginator.paginate(Bucket=bucket, Prefix='transacoes/'):
        if 'Contents' in page:
            for obj in page['Contents']:
                files.append(obj['Key'])
    
    print(f"📦 Encontrados {len(files)} arquivos brutos.")
    return files

def read_and_process_data(file_keys):
    """Lê JSONs do S3 e converte para DataFrame Pandas"""
    data_list = []
    
    print("⚙️ Lendo e processando arquivos (Isso simula o Spark)...")
    for key in file_keys:
        try:
            response = s3_client.get_object(Bucket=SOURCE_BUCKET, Key=key)
            content = response['Body'].read().decode('utf-8')
            # O Pandas lê o JSON direto
            df_temp = pd.read_json(io.StringIO(content), typ='series')
            data_list.append(df_temp)
        except Exception as e:
            print(f"Erro ao ler {key}: {e}")

    if not data_list:
        return pd.DataFrame()

    return pd.DataFrame(data_list)

def detect_fraud(df):
    """Aplica regras de negócio para encontrar fraudes"""
    if df.empty:
        return df

    print("🕵️  Analisando padrões de fraude...")
    
    # Regra 1: Transações muito altas (> R$ 8000)
    rule_high_value = df['valor'] > 8000
    
    # Regra 2: Estados suspeitos (Exemplo: transações do AC, RO, RR com valor > 2000)
    # Na vida real, isso viria de um modelo de Machine Learning
    rule_suspicious_location = (df['valor'] > 2000) & (df['estado'].isin(['AC', 'RO', 'RR']))
    
    # Filtra apenas o que atende às regras
    fraud_df = df[rule_high_value | rule_suspicious_location].copy()
    
    # Adiciona data de processamento
    fraud_df['processed_at'] = datetime.now()
    
    return fraud_df

def save_to_processed(df):
    """Salva o resultado em Parquet no S3 Processed"""
    if df.empty:
        print("👍 Nenhuma fraude detectada neste lote.")
        return

    # Nome do arquivo de saída (particionado por data)
    file_name = f"fraudes_detectadas/run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
    s3_path = f"s3://{TARGET_BUCKET}/{file_name}"
    
    print(f"💾 Salvando {len(df)} fraudes confirmadas em: {s3_path}")
    
    # Salva direto no S3 usando s3fs/pyarrow
    df.to_parquet(s3_path, index=False)
    print("✅ Processamento concluído com sucesso!")

if __name__ == "__main__":
    print("--- 🚀 Iniciando Job ETL de Fraude ---")
    
    # 1. Listar Arquivos
    files = get_files_from_s3(SOURCE_BUCKET)
    
    if len(files) > 0:
        # 2. Ler Dados
        df_raw = read_and_process_data(files)
        
        # 3. Detectar Fraude
        df_fraudes = detect_fraud(df_raw)
        
        print(f"📊 Resumo: {len(df_raw)} transações analisadas | {len(df_fraudes)} fraudes encontradas.")
        
        # 4. Salvar (Load)
        save_to_processed(df_fraudes)
    else:
        print("⚠️ Bucket Raw vazio. Rode o Producer primeiro!")