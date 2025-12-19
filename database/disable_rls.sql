-- =====================================================
-- SCRIPT COMPLETO: DESHABILITAR RLS Y LIMPIAR POLÍTICAS
-- Ejecutar en Supabase SQL Editor
-- =====================================================

-- =====================================================
-- PASO 1: ELIMINAR TRIGGERS DE AUDITORÍA
-- =====================================================

DROP TRIGGER IF EXISTS audit_pacientes ON pacientes;
DROP TRIGGER IF EXISTS audit_citas ON citas;
DROP TRIGGER IF EXISTS audit_indicadores ON indicadores_cita;
DROP TRIGGER IF EXISTS audit_diagnosticos ON diagnosticos_ia;

-- Eliminar función de auditoría
DROP FUNCTION IF EXISTS audit_trigger_function();

-- =====================================================
-- PASO 2: DESHABILITAR RLS EN TODAS LAS TABLAS
-- =====================================================

ALTER TABLE IF EXISTS pacientes DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS citas DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS indicadores_cita DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS diagnosticos_ia DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS metricas_ia DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS documentos_referencia DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS auditoria DISABLE ROW LEVEL SECURITY;

-- =====================================================
-- PASO 3: ELIMINAR TODAS LAS POLÍTICAS RLS
-- =====================================================

-- Políticas de pacientes
DROP POLICY IF EXISTS pacientes_select_policy ON pacientes;
DROP POLICY IF EXISTS pacientes_update_policy ON pacientes;
DROP POLICY IF EXISTS pacientes_insert_policy ON pacientes;
DROP POLICY IF EXISTS pacientes_delete_policy ON pacientes;

-- Políticas de citas
DROP POLICY IF EXISTS citas_select_policy ON citas;
DROP POLICY IF EXISTS citas_insert_policy ON citas;
DROP POLICY IF EXISTS citas_update_policy ON citas;

-- Políticas de indicadores
DROP POLICY IF EXISTS indicadores_select_policy ON indicadores_cita;
DROP POLICY IF EXISTS indicadores_insert_policy ON indicadores_cita;
DROP POLICY IF EXISTS indicadores_update_policy ON indicadores_cita;

-- Políticas de diagnósticos IA
DROP POLICY IF EXISTS diagnosticos_select_policy ON diagnosticos_ia;
DROP POLICY IF EXISTS diagnosticos_insert_policy ON diagnosticos_ia;

-- Políticas de documentos
DROP POLICY IF EXISTS documentos_select_policy ON documentos_referencia;
DROP POLICY IF EXISTS documentos_insert_policy ON documentos_referencia;
DROP POLICY IF EXISTS documentos_update_policy ON documentos_referencia;

-- Políticas de desarrollo (si existen)
DROP POLICY IF EXISTS "Allow all for development" ON pacientes;
DROP POLICY IF EXISTS "Allow all for development" ON citas;
DROP POLICY IF EXISTS "Allow all for development" ON indicadores_cita;
DROP POLICY IF EXISTS "Allow all for development" ON diagnosticos_ia;
DROP POLICY IF EXISTS "Allow all for development" ON metricas_ia;
DROP POLICY IF EXISTS "Allow all for development" ON documentos_referencia;
DROP POLICY IF EXISTS "Allow all for development" ON auditoria;

-- =====================================================
-- PASO 4: VERIFICACIÓN
-- =====================================================

-- Verificar que RLS está deshabilitado
SELECT 
    schemaname,
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY tablename;

-- Verificar que no hay políticas RLS
SELECT 
    schemaname,
    tablename,
    policyname
FROM pg_policies 
WHERE schemaname = 'public';

-- Si el resultado está vacío, ¡todo está limpio! ✅
