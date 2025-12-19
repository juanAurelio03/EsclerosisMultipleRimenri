"""
Test simple de permisos
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
service_key = os.getenv("SUPABASE_SERVICE_KEY")

print("TEST DE PERMISOS")
print("=" * 60)

client = create_client(url, service_key)

# Test SELECT
print("\nProbando SELECT...")
try:
    response = client.table('pacientes').select('*').limit(1).execute()
    print(f"✅ SELECT exitoso - {len(response.data)} registros")
except Exception as e:
    print(f"❌ Error: {e}")

# Test INSERT
print("\nProbando INSERT...")
try:
    test_data = {
        'nombre_completo': 'TEST',
        'edad': 25,
        'genero': 'Masculino',
        'tipo_em': 'EMRR',
        'edss_basal': 1.0,
        'fecha_diagnostico': '2024-01-01'
    }
    response = client.table('pacientes').insert(test_data).execute()
    print("✅ INSERT exitoso")
    
    # Limpiar
    if response.data:
        client.table('pacientes').delete().eq('id', response.data[0]['id']).execute()
        print("✅ DELETE exitoso")
except Exception as e:
    print(f"❌ Error: {e}")
    
print("\n" + "=" * 60)
print("\nSi ves errores arriba, el service_role key es incorrecto.")
print("Ve a Supabase → Settings → API y copia el 'service_role' key")
