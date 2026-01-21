import boto3
import json
import time
import uuid
import random
from faker import Faker
from datetime import datetime

# --- CONFIGURAÇÃO ---
# SUBSTITUA PELO NOME DO SEU BUCKET RAW (COPIE DO TERRAFORM OUTPUT)
BUCKET_NAME = "fraud-detection-raw-20260121180915898300000002" 
REGION = "us-east-1"

fake = Faker('pt_BR')
s3_client = boto3.client('s3', region_name=REGION)

def gerar_transacao():
    """Gera um dicionário simulando uma transação financeira"""
    return {
        "id_transacao": str(uuid.uuid4()),
        "cliente": fake.name(),
        "valor": round(random.uniform(10.0, 5000.0), 2),
        "cartao": fake.credit_card_number(),
        "cidade": fake.city(),
        "estado": fake.state_abbr(),
        "timestamp": datetime.now().isoformat(),
        "tipo_dispositivo": random.choice(['mobile', 'desktop', 'pos']),
        "flag_teste": True 
    }

def enviar_para_s3(dados):
    """Salva o JSON como um arquivo no S3"""
    # Nome do arquivo único para não sobrescrever
    file_name = f"transacoes/{dados['timestamp'][:10]}/{dados['id_transacao']}.json"
    
    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=json.dumps(dados),
            ContentType='application/json'
        )
        # Log visual simples
        simbolo = "🚨" if dados['valor'] > 2000 else "✅"
        print(f"[{simbolo}] Enviado: {dados['id_transacao']} | R$ {dados['valor']} | {dados['estado']}")
    except Exception as e:
        print(f"[X] Erro ao enviar: {e}")

if __name__ == "__main__":
    print(f"--- 🚀 Iniciando Gerador de Fraudes Batch (Destino: {BUCKET_NAME}) ---")
    print("Pressione CTRL+C para parar.\n")
    
    try:
        while True:
            transacao = gerar_transacao()
            
            # --- SIMULAÇÃO DE FRAUDE (Regra de Negócio) ---
            # 5% de chance de gerar uma transação muito alta fora de SP (padrão de fraude)
            if random.random() < 0.05: 
                transacao['valor'] = round(random.uniform(5000.0, 10000.0), 2)
                transacao['estado'] = random.choice(['AC', 'RO', 'RR']) # Estados aleatórios longe de SP
                print("   >>> GERANDO PADRÃO SUSPEITO <<<")

            enviar_para_s3(transacao)
            
            # Espera entre 0.5 e 2 segundos para variar o fluxo
            time.sleep(random.uniform(0.5, 2.0))
            
    except KeyboardInterrupt:
        print("\n🛑 Parando gerador...")