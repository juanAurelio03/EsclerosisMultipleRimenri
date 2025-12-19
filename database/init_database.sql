-- =====================================================
-- SCRIPT DE INICIALIZACIÓN COMPLETA
-- Ejecutar en Supabase SQL Editor
-- =====================================================

-- =====================================================
-- PASO 1: LIMPIAR BASE DE DATOS EXISTENTE
-- =====================================================

-- Eliminar triggers de auditoría si existen
DROP TRIGGER IF EXISTS audit_pacientes ON pacientes;
DROP TRIGGER IF EXISTS audit_citas ON citas;
DROP TRIGGER IF EXISTS audit_indicadores ON indicadores_cita;
DROP TRIGGER IF EXISTS audit_diagnosticos ON diagnosticos_ia;

-- Eliminar función de auditoría si existe
DROP FUNCTION IF EXISTS audit_trigger_function();

-- Deshabilitar RLS en todas las tablas
ALTER TABLE IF EXISTS pacientes DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS citas DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS indicadores_cita DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS diagnosticos_ia DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS metricas_ia DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS documentos_referencia DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS auditoria DISABLE ROW LEVEL SECURITY;

-- Eliminar todas las políticas RLS
DROP POLICY IF EXISTS pacientes_select_policy ON pacientes;
DROP POLICY IF EXISTS pacientes_update_policy ON pacientes;
DROP POLICY IF EXISTS pacientes_insert_policy ON pacientes;
DROP POLICY IF EXISTS pacientes_delete_policy ON pacientes;
DROP POLICY IF EXISTS citas_select_policy ON citas;
DROP POLICY IF EXISTS citas_insert_policy ON citas;
DROP POLICY IF EXISTS citas_update_policy ON citas;
DROP POLICY IF EXISTS indicadores_select_policy ON indicadores_cita;
DROP POLICY IF EXISTS indicadores_insert_policy ON indicadores_cita;
DROP POLICY IF EXISTS indicadores_update_policy ON indicadores_cita;
DROP POLICY IF EXISTS diagnosticos_select_policy ON diagnosticos_ia;
DROP POLICY IF EXISTS diagnosticos_insert_policy ON diagnosticos_ia;
DROP POLICY IF EXISTS documentos_select_policy ON documentos_referencia;
DROP POLICY IF EXISTS documentos_insert_policy ON documentos_referencia;
DROP POLICY IF EXISTS documentos_update_policy ON documentos_referencia;
DROP POLICY IF EXISTS "Allow all for development" ON pacientes;
DROP POLICY IF EXISTS "Allow all for development" ON citas;
DROP POLICY IF EXISTS "Allow all for development" ON indicadores_cita;
DROP POLICY IF EXISTS "Allow all for development" ON diagnosticos_ia;
DROP POLICY IF EXISTS "Allow all for development" ON metricas_ia;
DROP POLICY IF EXISTS "Allow all for development" ON documentos_referencia;
DROP POLICY IF EXISTS "Allow all for development" ON auditoria;

-- Eliminar tablas en orden correcto (respetando foreign keys)
DROP TABLE IF EXISTS auditoria CASCADE;
DROP TABLE IF EXISTS metricas_ia CASCADE;
DROP TABLE IF EXISTS documentos_referencia CASCADE;
DROP TABLE IF EXISTS diagnosticos_ia CASCADE;
DROP TABLE IF EXISTS indicadores_cita CASCADE;
DROP TABLE IF EXISTS citas CASCADE;
DROP TABLE IF EXISTS pacientes CASCADE;

-- Eliminar tipos ENUM
DROP TYPE IF EXISTS ia_seleccionada CASCADE;
DROP TYPE IF EXISTS estado_indicador CASCADE;
DROP TYPE IF EXISTS indicador_tipo CASCADE;

-- =====================================================
-- PASO 2: CREAR EXTENSIONES
-- =====================================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- PASO 3: CREAR TIPOS ENUM
-- =====================================================
CREATE TYPE indicador_tipo AS ENUM ('ARR', 'T1_Gd', 'T2_nuevas', 'CDP12', 'NEDA3');
CREATE TYPE estado_indicador AS ENUM ('normal', 'alerta', 'critico');
CREATE TYPE ia_seleccionada AS ENUM ('deepseek', 'copilot', 'medico');

-- =====================================================
-- PASO 4: CREAR TABLAS
-- =====================================================

-- TABLA: pacientes
CREATE TABLE pacientes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre_completo VARCHAR(255) NOT NULL,
    edad INTEGER NOT NULL CHECK (edad > 0 AND edad < 120),
    genero VARCHAR(50) NOT NULL,
    tipo_em VARCHAR(10) NOT NULL CHECK (tipo_em IN ('EMRR', 'EMSP', 'EMPP')),
    edss_basal DECIMAL(3,1) NOT NULL CHECK (edss_basal >= 0 AND edss_basal <= 10),
    tratamiento_actual VARCHAR(255),
    fecha_diagnostico DATE NOT NULL,
    historial_medico JSONB DEFAULT '{}',
    medico_asignado_id UUID,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- TABLA: citas
CREATE TABLE citas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    paciente_id UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    fecha_cita TIMESTAMP WITH TIME ZONE NOT NULL,
    numero_visita INTEGER NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'completada', 'cancelada')),
    notas_medicas TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(paciente_id, numero_visita)
);

-- TABLA: indicadores_cita
CREATE TABLE indicadores_cita (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cita_id UUID NOT NULL REFERENCES citas(id) ON DELETE CASCADE,
    indicador_tipo indicador_tipo NOT NULL,
    valor_calculado DECIMAL(10,2),
    estado estado_indicador NOT NULL,
    justificacion_texto TEXT NOT NULL,
    variables_entrada JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(cita_id, indicador_tipo)
);

-- TABLA: diagnosticos_ia
CREATE TABLE diagnosticos_ia (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cita_id UUID NOT NULL REFERENCES citas(id) ON DELETE CASCADE,
    diagnostico_deepseek TEXT,
    confianza_deepseek DECIMAL(3,1) CHECK (confianza_deepseek >= 0 AND confianza_deepseek <= 10),
    diagnostico_copilot TEXT,
    confianza_copilot DECIMAL(3,1) CHECK (confianza_copilot >= 0 AND confianza_copilot <= 10),
    ia_seleccionada ia_seleccionada NOT NULL,
    diagnostico_medico_override TEXT,
    justificacion_medico TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(cita_id)
);

-- TABLA: metricas_ia
CREATE TABLE metricas_ia (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fecha_calculo DATE NOT NULL,
    total_consultas INTEGER NOT NULL DEFAULT 0,
    selecciones_deepseek INTEGER NOT NULL DEFAULT 0,
    selecciones_copilot INTEGER NOT NULL DEFAULT 0,
    selecciones_medico_override INTEGER NOT NULL DEFAULT 0,
    accuracy_deepseek DECIMAL(5,2),
    accuracy_copilot DECIMAL(5,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(fecha_calculo)
);

-- TABLA: documentos_referencia
CREATE TABLE documentos_referencia (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre_archivo VARCHAR(255) NOT NULL,
    contenido_extraido TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- TABLA: auditoria
CREATE TABLE auditoria (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tabla_afectada VARCHAR(100) NOT NULL,
    registro_id UUID NOT NULL,
    accion VARCHAR(20) NOT NULL CHECK (accion IN ('INSERT', 'UPDATE', 'DELETE')),
    usuario_id UUID,
    datos_anteriores JSONB,
    datos_nuevos JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- PASO 5: CREAR ÍNDICES
-- =====================================================

-- Índices para pacientes
CREATE INDEX idx_pacientes_nombre ON pacientes(nombre_completo);
CREATE INDEX idx_pacientes_medico ON pacientes(medico_asignado_id);
CREATE INDEX idx_pacientes_activo ON pacientes(activo);

-- Índices para citas
CREATE INDEX idx_citas_paciente ON citas(paciente_id);
CREATE INDEX idx_citas_fecha ON citas(fecha_cita);
CREATE INDEX idx_citas_estado ON citas(estado);

-- Índices para indicadores
CREATE INDEX idx_indicadores_cita ON indicadores_cita(cita_id);
CREATE INDEX idx_indicadores_tipo ON indicadores_cita(indicador_tipo);
CREATE INDEX idx_indicadores_estado ON indicadores_cita(estado);

-- Índices para diagnósticos IA
CREATE INDEX idx_diagnosticos_cita ON diagnosticos_ia(cita_id);
CREATE INDEX idx_diagnosticos_ia_seleccionada ON diagnosticos_ia(ia_seleccionada);

-- Índices para métricas IA
CREATE INDEX idx_metricas_fecha ON metricas_ia(fecha_calculo);

-- Índices para documentos
CREATE INDEX idx_documentos_activo ON documentos_referencia(activo);

-- Índices para auditoría
CREATE INDEX idx_auditoria_tabla ON auditoria(tabla_afectada);
CREATE INDEX idx_auditoria_timestamp ON auditoria(timestamp);
CREATE INDEX idx_auditoria_usuario ON auditoria(usuario_id);

-- =====================================================
-- PASO 6: CREAR TRIGGERS (solo updated_at)
-- =====================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_pacientes_updated_at BEFORE UPDATE ON pacientes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_citas_updated_at BEFORE UPDATE ON citas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_documentos_updated_at BEFORE UPDATE ON documentos_referencia
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- PASO 7: COMENTARIOS
-- =====================================================

COMMENT ON TABLE pacientes IS 'Almacena información demográfica y clínica de pacientes con Esclerosis Múltiple';
COMMENT ON TABLE citas IS 'Registro de citas progresivas de seguimiento';
COMMENT ON TABLE indicadores_cita IS 'Indicadores clínicos calculados por cita (ARR, EDSS, NEDA-3, etc.)';
COMMENT ON TABLE diagnosticos_ia IS 'Diagnósticos generados por IAs y selección del médico';
COMMENT ON TABLE metricas_ia IS 'Métricas de precisión de las IAs a lo largo del tiempo';
COMMENT ON TABLE documentos_referencia IS 'Artículos científicos de referencia para contexto de IA';
COMMENT ON TABLE auditoria IS 'Log de auditoría para compliance HIPAA/GDPR';

-- =====================================================
-- VERIFICACIÓN FINAL
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

-- Mostrar resumen de tablas creadas
SELECT 
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as num_columns
FROM information_schema.tables t
WHERE table_schema = 'public'
AND table_type = 'BASE TABLE'
ORDER BY table_name;
