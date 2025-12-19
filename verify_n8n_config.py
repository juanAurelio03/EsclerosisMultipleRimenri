import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add root to path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

load_dotenv()

from src.n8n.n8n_client import n8n_client

print("="*50)
print("VERIFICACIÓN DE CONFIGURACIÓN N8N")
print("="*50)

print(f"N8N_AI_WEBHOOK: {n8n_client.ai_webhook_url}")
print(f"N8N_ALERT_WEBHOOK: {n8n_client.alert_webhook_url}")

if n8n_client.is_configured():
    print("\n✅ n8n_client está configurado correctamente.")
else:
    print("\n❌ n8n_client NO está configurado correctamente.")

if n8n_client.ai_webhook_url == "https://unmusked-trailingly-louis.ngrok-free.dev/webhook-test/ai-consultation":
    print("✅ URL de Webhook correcta.")
else:
    print("❌ URL de Webhook incorrecta.")
