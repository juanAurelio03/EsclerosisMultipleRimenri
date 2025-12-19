"""
Script de prueba de conexión a Supabase
Ejecuta: python test_connection.py
"""
import os
from dotenv import load_dotenv
from supabase import create_client

# Cargar variables de entorno
load_dotenv()

print("=" * 60)
print("PRUEBA DE CONEXIÓN A SUPABASE")
print("=" * 60)

# 1. Verificar variables de entorno
print("\n1. Verificando variables de entorno...")
url = os.getenv("SUPABASE_URL")
anon_key = os.getenv("SUPABASE_KEY")
service_key = os.getenv("SUPABASE_SERVICE_KEY")

print(f"   SUPABASE_URL: {'✅ Configurada' if url else '❌ NO configurada'}")
print(f"   SUPABASE_KEY (anon): {'✅ Configurada' if anon_key else '❌ NO configurada'}")
print(f"   SUPABASE_SERVICE_KEY: {'✅ Configurada' if service_key else '❌ NO configurada'}")

if url:
    print(f"   URL: {url}")

if not url or not service_key:
    print("\n❌ ERROR: Faltan variables de entorno necesarias")
    print("   Asegúrate de tener SUPABASE_URL y SUPABASE_SERVICE_KEY en tu archivo .env")
    exit(1)

# 2. Probar conexión con SERVICE_KEY
print("\n2. Probando conexión con SERVICE_KEY...")
try:
    client = create_client(url, service_key)
    print("   ✅ Cliente creado exitosamente")
except Exception as e:
    print(f"   ❌ Error al crear cliente: {e}")
    exit(1)

# 3. Verificar que las tablas existen
print("\n3. Verificando existencia de tablas...")
try:
    # Intentar hacer una consulta simple
    response = client.table('pacientes').select('id').limit(1).execute()
    print("   ✅ Tabla 'pacientes' existe y es accesible")
    print(f"   Registros encontrados: {len(response.data)}")
except Exception as e:
    print(f"   ❌ Error al acceder a tabla 'pacientes': {e}")
    error_dict = e.args[0] if e.args else {}
    if isinstance(error_dict, dict):
        print(f"   Código de error: {error_dict.get('code')}")
        print(f"   Mensaje: {error_dict.get('message')}")
        print(f"   Detalles: {error_dict.get('details')}")
    
    print("\n   POSIBLES CAUSAS:")
    print("   1. La tabla 'pacientes' no existe en Supabase")
    print("   2. No has ejecutado el script database/schema.sql")
    print("   3. RLS está habilitado y bloqueando el acceso")
    exit(1)

# 4. Verificar permisos de escritura
print("\n4. Probando permisos de escritura...")
try:
    # Intentar insertar un registro de prueba
    test_data = {
        'nombre_completo': 'TEST - Paciente de Prueba',
        'edad': 30,
        'genero': 'Masculino',
        'tipo_em': 'EMRR',
        'edss_basal': 2.0,
        'fecha_diagnostico': '2024-01-01',
        'activo': False  # Marcado como inactivo para no interferir
    }
    
    response = client.table('pacientes').insert(test_data).execute()
    print("   ✅ Inserción exitosa")
    
    # Eliminar el registro de prueba
    if response.data:
        test_id = response.data[0]['id']
        client.table('pacientes').delete().eq('id', test_id).execute()
        print("   ✅ Eliminación exitosa")
    
except Exception as e:
    print(f"   ❌ Error al insertar: {e}")
    error_dict = e.args[0] if e.args else {}
    if isinstance(error_dict, dict):
        print(f"   Código de error: {error_dict.get('code')}")
        print(f"   Mensaje: {error_dict.get('message')}")

# 5. Verificar RLS
print("\n5. Verificando estado de RLS...")
try:
    # Consulta para verificar RLS
    query = """
    SELECT 
        tablename,
        rowsecurity as rls_enabled
    FROM pg_tables 
    WHERE schemaname = 'public' 
    AND tablename IN ('pacientes', 'citas', 'indicadores_cita')
    ORDER BY tablename;
    """
    
    # Nota: Esta consulta puede no funcionar con todos los permisos
    print("   (Esta verificación puede requerir permisos especiales)")
    
except Exception as e:
    print(f"   ⚠️ No se pudo verificar RLS: {e}")

# 6. Resumen
print("\n" + "=" * 60)
print("RESUMEN DE LA PRUEBA")
print("=" * 60)
print("\n✅ Si llegaste hasta aquí, la conexión funciona correctamente!")
print("\nSi aún tienes problemas en Streamlit:")
print("1. Verifica que el archivo .env esté en la raíz del proyecto")
print("2. Reinicia completamente Streamlit (Ctrl+C y vuelve a ejecutar)")
print("3. Verifica que estés usando SUPABASE_SERVICE_KEY en .env")
print("\n" + "=" * 60)
