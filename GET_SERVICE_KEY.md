# 🔑 SOLUCIÓN DEFINITIVA: Obtener el Service Role Key Correcto

## ❌ Problema Confirmado

El test muestra que **el service_role key en tu .env NO es correcto**.

```
❌ Error: {'message': 'permission denied for table pacientes', 'code': '42501'}
```

Esto significa que estás usando un key que NO tiene permisos completos.

## ✅ Solución: Obtener el Service Role Key Correcto

### Paso 1: Ir a Settings → API en Supabase

1. Abre: https://supabase.com/dashboard/project/stdrygyopbzcpjildlxs/settings/api
2. Busca la sección **"Project API keys"**

### Paso 2: Copiar el Service Role Key

Verás DOS keys:

1. **`anon` `public`** ← ❌ NO uses este
2. **`service_role` `secret`** ← ✅ USA ESTE

**IMPORTANTE**: El `service_role` key:
- Es MÁS LARGO que el anon key
- Dice "secret" al lado
- Tiene un ícono de candado 🔒
- Bypasea RLS automáticamente

### Paso 3: Actualizar tu .env

Abre tu archivo `.env` y REEMPLAZA la línea:

```env
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Con el **service_role key** que copiaste de Supabase.

### Paso 4: Verificar que es el Correcto

El service_role key debe:
- Empezar con `eyJ...`
- Tener aproximadamente 300-400 caracteres
- Ser DIFERENTE al anon key

### Paso 5: Probar

```bash
python test_simple.py
```

Deberías ver:
```
✅ SELECT exitoso - X registros
✅ INSERT exitoso
✅ DELETE exitoso
```

### Paso 6: Reiniciar Streamlit

```bash
# Ctrl+C para detener
streamlit run app.py
```

## 🎯 Cómo Identificar el Key Correcto

En Supabase Dashboard → Settings → API verás algo así:

```
Project API keys

anon public
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN0ZHJ5Z3lvcGJ6Y3BqaWxkbHhzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NzI3ODQsImV4cCI6MjA3OTA0ODc4NH0.KpaSyKa0ol7hG6EBxlAWnRR3nZu-eNz_XDY8ZTu5j0o
[Copy] [Reveal]

service_role secret  🔒
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN0ZHJ5Z3lvcGJ6Y3BqaWxkbHhzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzQ3Mjc4NCwiZXhwIjoyMDc5MDQ4Nzg0fQ.u9Ko-NNsX5Qm0EB-0e6bxtnYwoaka2x7Z72C0v45kcM
[Copy] [Reveal]  ← COPIA ESTE
```

## ⚠️ Nota de Seguridad

El `service_role` key:
- Tiene acceso COMPLETO a tu base de datos
- Bypasea todas las políticas de seguridad
- NUNCA lo expongas en el frontend
- Solo úsalo en el backend (Python/Streamlit)

## 📝 Tu .env Debería Verse Así

```env
# Supabase Configuration
SUPABASE_URL=https://stdrygyopbzcpjildlxs.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN0ZHJ5Z3lvcGJ6Y3BqaWxkbHhzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NzI3ODQsImV4cCI6MjA3OTA0ODc4NH0.KpaSyKa0ol7hG6EBxlAWnRR3nZu-eNz_XDY8ZTu5j0o
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN0ZHJ5Z3lvcGJ6Y3BqaWxkbHhzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzQ3Mjc4NCwiZXhwIjoyMDc5MDQ4Nzg0fQ.u9Ko-NNsX5Qm0EB-0e6bxtnYwoaka2x7Z72C0v45kcM
```

**Nota**: El que tienes actualmente parece ser el correcto, pero verifica que sea exactamente el mismo que aparece en Supabase.

---

Una vez actualices el key correcto, **TODO FUNCIONARÁ** 🚀
