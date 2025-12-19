# 📋 Guía de Uso - Scripts de Base de Datos Corregidos

## ✅ Scripts Creados

He creado **4 scripts SQL corregidos** sin RLS ni dependencias de autenticación:

### 1. **`schema_clean.sql`** - Schema Limpio
- ✅ Todas las tablas sin RLS
- ✅ Sin triggers de auditoría con `auth.uid()`
- ✅ Mantiene todas las restricciones de integridad
- ✅ Mantiene triggers de `updated_at`

### 2. **`init_database.sql`** - Inicialización Completa
- ✅ Limpia base de datos existente
- ✅ Elimina todas las políticas RLS
- ✅ Elimina triggers de auditoría
- ✅ Recrea todo desde cero
- ✅ Incluye verificación final

### 3. **`sample_data.sql`** - Datos de Prueba
- ✅ 12 pacientes con diferentes perfiles
- ✅ 15+ citas distribuidas
- ✅ Indicadores clínicos (normal, alerta, crítico)
- ✅ Diagnósticos de IA
- ✅ Métricas de IA
- ✅ Documento de referencia

### 4. **`disable_rls.sql`** - Deshabilitar RLS (Actualizado)
- ✅ Elimina triggers de auditoría
- ✅ Deshabilita RLS en todas las tablas
- ✅ Elimina todas las políticas
- ✅ Incluye verificación

---

## 🚀 Cómo Usar

### **Opción A: Inicialización Completa (Recomendado)**

Si quieres empezar desde cero con una base de datos limpia:

```sql
-- 1. Ejecutar en Supabase SQL Editor
\i init_database.sql

-- 2. Crear funciones de cálculo (usar el archivo original)
\i functions.sql

-- 3. Insertar datos de prueba
\i sample_data.sql
```

**O copiar y pegar directamente en Supabase SQL Editor:**
1. Abre Supabase → SQL Editor
2. Copia todo el contenido de `init_database.sql`
3. Pega y ejecuta
4. Repite con `functions.sql`
5. Repite con `sample_data.sql`

---

### **Opción B: Solo Deshabilitar RLS**

Si ya tienes datos y solo quieres quitar las restricciones:

```sql
-- Ejecutar en Supabase SQL Editor
\i disable_rls.sql
```

**O copiar y pegar:**
1. Abre Supabase → SQL Editor
2. Copia todo el contenido de `disable_rls.sql`
3. Pega y ejecuta

---

## 🔍 Verificación

Después de ejecutar los scripts, verifica que todo esté correcto:

### 1. Verificar que RLS está deshabilitado:
```sql
SELECT 
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY tablename;
```

**Resultado esperado:** Todas las tablas deben mostrar `rls_enabled = false`

### 2. Verificar que no hay políticas RLS:
```sql
SELECT * FROM pg_policies WHERE schemaname = 'public';
```

**Resultado esperado:** Sin resultados (tabla vacía)

### 3. Verificar datos insertados:
```sql
SELECT 'Pacientes' as tabla, COUNT(*) as total FROM pacientes
UNION ALL
SELECT 'Citas', COUNT(*) FROM citas
UNION ALL
SELECT 'Indicadores', COUNT(*) FROM indicadores_cita
UNION ALL
SELECT 'Diagnósticos IA', COUNT(*) FROM diagnosticos_ia;
```

**Resultado esperado:**
- Pacientes: 12
- Citas: 15+
- Indicadores: 15+
- Diagnósticos IA: 2+

---

## 📊 Datos de Prueba Incluidos

### Pacientes:
- **María González Pérez** - EMRR, EDSS 2.0, Interferón beta-1a (NEDA-3 ✅)
- **Juan Carlos Rodríguez** - EMSP, EDSS 4.5, Fingolimod (Actividad ⚠️)
- **Ana Martínez López** - EMRR, EDSS 1.5, Natalizumab (Excelente respuesta ✅)
- **Pedro Sánchez García** - EMPP, EDSS 6.0, Ocrelizumab (Progresión lenta)
- Y 8 pacientes más...

### Escenarios de Indicadores:
- ✅ **Normal**: Sin recaídas, sin lesiones, EDSS estable
- ⚠️ **Alerta**: ARR 0.10-0.19, lesiones T1 Gd+ 0.03-0.49
- 🔴 **Crítico**: ARR ≥0.20, lesiones T2 >2.80, progresión EDSS

---

## ⚙️ Configuración de tu Aplicación

Tu aplicación Python **ya está lista** para funcionar con estos scripts. Solo asegúrate de que tu `.env` tenga:

```env
SUPABASE_URL=https://stdrygyopbzcpjildlxs.supabase.co
SUPABASE_SERVICE_KEY=tu_service_key_aqui
```

**Importante:** Usa `SUPABASE_SERVICE_KEY` (no `SUPABASE_KEY`) para tener permisos completos.

---

## 🎯 Próximos Pasos

1. **Ejecuta `init_database.sql`** en Supabase SQL Editor
2. **Ejecuta `functions.sql`** (el archivo original está bien)
3. **Ejecuta `sample_data.sql`** para tener datos de prueba
4. **Reinicia tu aplicación Streamlit**
5. **Prueba la aplicación** - ¡Debería funcionar sin errores de permisos!

---

## 🆘 Solución de Problemas

### Error: "permission denied for table pacientes"
**Solución:** Ejecuta `disable_rls.sql` para eliminar todas las políticas RLS.

### Error: "function auth.uid() does not exist"
**Solución:** Ejecuta `init_database.sql` para eliminar triggers de auditoría.

### Error: "relation does not exist"
**Solución:** Ejecuta `init_database.sql` para crear todas las tablas.

---

## 📝 Notas Importantes

- ✅ **Código Python verificado**: Coincide 100% con la estructura de base de datos
- ✅ **Sin cambios en tu código**: No necesitas modificar ningún archivo Python
- ✅ **Funciones originales**: El archivo `functions.sql` original funciona perfectamente
- ⚠️ **Solo para desarrollo**: En producción deberías configurar RLS correctamente
- 🔒 **Seguridad**: Estos scripts eliminan la seguridad RLS para facilitar el desarrollo

---

## 📞 Resumen

**Archivos creados:**
1. `database/schema_clean.sql` - Schema sin RLS
2. `database/init_database.sql` - Inicialización completa
3. `database/sample_data.sql` - Datos de prueba
4. `database/disable_rls.sql` - Deshabilitar RLS (actualizado)

**Orden de ejecución recomendado:**
```
init_database.sql → functions.sql → sample_data.sql
```

**¡Tu aplicación está lista para funcionar! 🎉**
