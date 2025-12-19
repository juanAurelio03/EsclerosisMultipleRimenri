"""
Test específico de permisos en Supabase
"""
import os
from dotenv import load_dotenv
from supabase import create_client
import json

load_dotenv()

url = os.getenv("SUPABASE_URL")
service_key = os.getenv("SUPABASE_SERVICE_KEY")

print("=" * 60)
print("TEST DE PERMISOS ESPECÍFICOS")
print("=" * 60)

# Crear cliente
client = create_client(url, service_key)

# Test 1: SELECT
print("\n1. Probando SELECT...")
try:
    response = client.table('pacientes').select('*').limit(5).execute()
    print(f"   ✅ SELECT exitoso - {len(response.data)} registros")
    if response.data:
        print(f"   Primer paciente: {response.data[0].get('nombre_completo', 'N/A')}")
except Exception as e:
    print(f"   ❌ Error en SELECT: {e}")
    print(f"   Detalles: {json.dumps(e.args[0] if e.args else {}, indent=2)}")

# Test 2: INSERT
print("\n2. Probando INSERT...")
try:
    test_data = {
        'nombre_completo': 'TEST Paciente',
        'edad': 25,
        'genero': 'Masculino',
        'tipo_em': 'EMRR',
        'edss_basal': 1.0,
        'fecha_diagnostico': '2024-01-01',
        'activo': False
    }
    response = client.table('pacientes').insert(test_data).execute()
    print(f"   ✅ INSERT exitoso")
    test_id = response.data[0]['id'] if response.data else None
    
    # Test 3: DELETE (limpiar)
    if test_id:
        print("\n3. Probando DELETE...")
        client.table('pacientes').delete().eq('id', test_id).execute()
        print(f"   ✅ DELETE exitoso")
        
except Exception as e:
    print(f"   ❌ Error en INSERT: {e}")
    error_data = e.args[0] if e.args else {}
    print(f"   Código: {error_data.get('code')}")
    print(f"   Mensaje: {error_data.get('message')}")
    
    # Diagnóstico adicional
    if error_data.get('code') == '42501':
        print("\n   🔍 DIAGNÓSTICO:")
        print("   El código 42501 significa 'insufficient_privilege'")
        print("   Esto indica que el service_role key NO tiene permisos")
        print("\n   POSIBLES CAUSAS:")
        print("   1. El service_role key es incorrecto")
        print("   2. Hay políticas RLS que aún están activas")
        print("   3. El usuario de la API no tiene permisos GRANT")
        
        print("\n   SOLUCIÓN:")
        print("   Ve a Supabase Dashboard → Settings → API")
        print("   Copia el 'service_role' key (NO el 'anon public')")
        print("   Reemplaza SUPABASE_SERVICE_KEY en tu .env")

print("\n" + "=" * 60)
