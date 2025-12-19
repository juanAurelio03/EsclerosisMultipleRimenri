"""
Script para verificar qué key se está usando
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("VERIFICACIÓN DE KEYS")
print("=" * 60)

url = os.getenv("SUPABASE_URL")
anon_key = os.getenv("SUPABASE_KEY")
service_key = os.getenv("SUPABASE_SERVICE_KEY")

print(f"\nSUPABASE_URL: {url}")
print(f"\nSUPABASE_KEY (anon): {anon_key[:50]}..." if anon_key else "❌ NO configurada")
print(f"\nSUPABASE_SERVICE_KEY: {service_key[:50]}..." if service_key else "❌ NO configurada")

# Verificar cuál se está usando
key_to_use = service_key or anon_key
print(f"\n{'='*60}")
print(f"KEY QUE SE USARÁ: {'SERVICE_KEY ✅' if service_key else 'ANON_KEY ⚠️'}")
print(f"{'='*60}")

if not service_key:
    print("\n❌ PROBLEMA ENCONTRADO:")
    print("   SUPABASE_SERVICE_KEY no está configurada en .env")
    print("\n✅ SOLUCIÓN:")
    print("   Agrega esta línea a tu archivo .env:")
    print(f"   SUPABASE_SERVICE_KEY={anon_key}")
    print("\n   (Nota: Usa el service_role key de Supabase, no el anon key)")
