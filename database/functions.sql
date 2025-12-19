-- =====================================================
-- FUNCIONES DE CÁLCULO DE INDICADORES CLÍNICOS
-- =====================================================

-- =====================================================
-- FUNCIÓN: calcular_arr
-- Calcula la Tasa Anualizada de Recaídas (ARR)
-- =====================================================
CREATE OR REPLACE FUNCTION calcular_arr(
    p_paciente_id UUID,
    p_fecha_inicio TIMESTAMP WITH TIME ZONE,
    p_fecha_fin TIMESTAMP WITH TIME ZONE
)
RETURNS TABLE(
    arr_valor DECIMAL(10,2),
    estado estado_indicador,
    justificacion TEXT
) AS $$
DECLARE
    v_total_recaidas INTEGER;
    v_anos_paciente DECIMAL(10,2);
    v_arr DECIMAL(10,2);
    v_estado estado_indicador;
    v_justificacion TEXT;
BEGIN
    -- Contar recaídas en el período
    SELECT COALESCE(SUM((variables_entrada->>'recaidas')::INTEGER), 0)
    INTO v_total_recaidas
    FROM indicadores_cita ic
    JOIN citas c ON ic.cita_id = c.id
    WHERE c.paciente_id = p_paciente_id
      AND c.fecha_cita BETWEEN p_fecha_inicio AND p_fecha_fin
      AND ic.indicador_tipo = 'ARR';
    
    -- Calcular años-paciente
    v_anos_paciente := EXTRACT(EPOCH FROM (p_fecha_fin - p_fecha_inicio)) / (365.25 * 24 * 60 * 60);
    
    -- Evitar división por cero
    IF v_anos_paciente = 0 THEN
        v_anos_paciente := 1;
    END IF;
    
    -- Calcular ARR
    v_arr := v_total_recaidas / v_anos_paciente;
    
    -- Clasificar según rangos
    IF v_arr >= 0.20 THEN
        v_estado := 'critico';
        v_justificacion := format('⚠️ CRÍTICO: ARR de %.2f supera el umbral de 0.20, indicando fallo terapéutico. Se recomienda evaluar cambio de DMT o escalada terapéutica.', v_arr);
    ELSIF v_arr >= 0.10 THEN
        v_estado := 'alerta';
        v_justificacion := format('⚠️ ALERTA: ARR de %.2f está en rango de alerta (0.10-0.19). Requiere monitoreo cercano y evaluación de eficacia del tratamiento actual.', v_arr);
    ELSE
        v_estado := 'normal';
        v_justificacion := format('✓ NORMAL: ARR de %.2f está dentro del rango óptimo (<0.10). El tratamiento actual muestra buena eficacia en control de recaídas.', v_arr);
    END IF;
    
    RETURN QUERY SELECT v_arr, v_estado, v_justificacion;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- FUNCIÓN: clasificar_t1_gd
-- Clasifica lesiones T1 con gadolinio
-- =====================================================
CREATE OR REPLACE FUNCTION clasificar_t1_gd(
    p_conteo_lesiones INTEGER
)
RETURNS TABLE(
    estado estado_indicador,
    justificacion TEXT
) AS $$
DECLARE
    v_estado estado_indicador;
    v_justificacion TEXT;
BEGIN
    IF p_conteo_lesiones >= 0.50 THEN
        v_estado := 'critico';
        v_justificacion := format('⚠️ CRÍTICO: %s lesiones T1 Gd+ detectadas (≥0.50). Indica inflamación activa severa del SNC. Requiere intervención inmediata.', p_conteo_lesiones);
    ELSIF p_conteo_lesiones >= 0.03 THEN
        v_estado := 'alerta';
        v_justificacion := format('⚠️ ALERTA: %s lesiones T1 Gd+ detectadas (0.03-0.49). Indica actividad inflamatoria que requiere monitoreo cercano.', p_conteo_lesiones);
    ELSE
        v_estado := 'normal';
        v_justificacion := format('✓ NORMAL: %s lesiones T1 Gd+ detectadas (<0.03). Sin evidencia significativa de inflamación activa.', p_conteo_lesiones);
    END IF;
    
    RETURN QUERY SELECT v_estado, v_justificacion;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- FUNCIÓN: calcular_diferencia_t2
-- Calcula nuevas lesiones T2 o agrandadas
-- =====================================================
CREATE OR REPLACE FUNCTION calcular_diferencia_t2(
    p_t2_actual INTEGER,
    p_t2_previo INTEGER
)
RETURNS TABLE(
    diferencia INTEGER,
    estado estado_indicador,
    justificacion TEXT
) AS $$
DECLARE
    v_diferencia INTEGER;
    v_estado estado_indicador;
    v_justificacion TEXT;
BEGIN
    v_diferencia := p_t2_actual - p_t2_previo;
    
    IF v_diferencia > 2.80 THEN
        v_estado := 'critico';
        v_justificacion := format('⚠️ CRÍTICO: %s nuevas lesiones T2 detectadas (>2.80). Indica progresión significativa de carga lesional. Evaluar cambio de tratamiento.', v_diferencia);
    ELSIF v_diferencia >= 0.31 THEN
        v_estado := 'alerta';
        v_justificacion := format('⚠️ ALERTA: %s nuevas lesiones T2 detectadas (0.31-2.80). Requiere evaluación de eficacia terapéutica.', v_diferencia);
    ELSE
        v_estado := 'normal';
        v_justificacion := format('✓ NORMAL: %s nuevas lesiones T2 (≤0.30). Carga lesional estable.', v_diferencia);
    END IF;
    
    RETURN QUERY SELECT v_diferencia, v_estado, v_justificacion;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- FUNCIÓN: evaluar_cdp12
-- Evalúa Confirmed Disability Progression a 12 semanas
-- =====================================================
CREATE OR REPLACE FUNCTION evaluar_cdp12(
    p_edss_basal DECIMAL(3,1),
    p_edss_actual DECIMAL(3,1)
)
RETURNS TABLE(
    delta_edss DECIMAL(3,1),
    progresion_confirmada BOOLEAN,
    estado estado_indicador,
    justificacion TEXT
) AS $$
DECLARE
    v_delta DECIMAL(3,1);
    v_progresion BOOLEAN;
    v_estado estado_indicador;
    v_justificacion TEXT;
    v_umbral DECIMAL(3,1);
BEGIN
    v_delta := p_edss_actual - p_edss_basal;
    
    -- Determinar umbral según EDSS basal
    IF p_edss_basal <= 5.5 THEN
        v_umbral := 1.0;
    ELSE
        v_umbral := 0.5;
    END IF;
    
    -- Evaluar progresión
    v_progresion := v_delta >= v_umbral;
    
    IF v_progresion THEN
        v_estado := 'critico';
        v_justificacion := format('⚠️ CRÍTICO: CDP-12 confirmado. ΔEDSS = %.1f (umbral: %.1f para EDSS basal %.1f). Progresión de discapacidad confirmada. Requiere revisión urgente del plan terapéutico.', v_delta, v_umbral, p_edss_basal);
    ELSIF v_delta > 0 THEN
        v_estado := 'alerta';
        v_justificacion := format('⚠️ ALERTA: ΔEDSS = %.1f positivo pero no alcanza umbral CDP-12 (%.1f). Monitorear evolución en próximas visitas.', v_delta, v_umbral);
    ELSE
        v_estado := 'normal';
        v_justificacion := format('✓ NORMAL: ΔEDSS = %.1f. Sin progresión de discapacidad. EDSS estable o mejorado.', v_delta);
    END IF;
    
    RETURN QUERY SELECT v_delta, v_progresion, v_estado, v_justificacion;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- FUNCIÓN: evaluar_neda3
-- Evalúa No Evidence of Disease Activity (NEDA-3)
-- =====================================================
CREATE OR REPLACE FUNCTION evaluar_neda3(
    p_cita_id UUID
)
RETURNS TABLE(
    cumple_neda3 BOOLEAN,
    estado estado_indicador,
    justificacion TEXT,
    detalles JSONB
) AS $$
DECLARE
    v_sin_recaidas BOOLEAN;
    v_sin_lesiones_rm BOOLEAN;
    v_sin_progresion_edss BOOLEAN;
    v_cumple BOOLEAN;
    v_estado estado_indicador;
    v_justificacion TEXT;
    v_detalles JSONB;
BEGIN
    -- Verificar criterio 1: Sin recaídas
    SELECT COALESCE((variables_entrada->>'recaidas')::INTEGER, 0) = 0
    INTO v_sin_recaidas
    FROM indicadores_cita
    WHERE cita_id = p_cita_id AND indicador_tipo = 'ARR';
    
    -- Verificar criterio 2: Sin nuevas lesiones en RM
    SELECT estado IN ('normal')
    INTO v_sin_lesiones_rm
    FROM indicadores_cita
    WHERE cita_id = p_cita_id 
      AND indicador_tipo IN ('T1_Gd', 'T2_nuevas')
    LIMIT 1;
    
    -- Verificar criterio 3: Sin progresión de EDSS
    SELECT estado IN ('normal')
    INTO v_sin_progresion_edss
    FROM indicadores_cita
    WHERE cita_id = p_cita_id AND indicador_tipo = 'CDP12';
    
    -- Evaluar NEDA-3
    v_cumple := COALESCE(v_sin_recaidas, FALSE) 
                AND COALESCE(v_sin_lesiones_rm, FALSE) 
                AND COALESCE(v_sin_progresion_edss, FALSE);
    
    -- Construir detalles
    v_detalles := jsonb_build_object(
        'sin_recaidas', COALESCE(v_sin_recaidas, FALSE),
        'sin_lesiones_rm', COALESCE(v_sin_lesiones_rm, FALSE),
        'sin_progresion_edss', COALESCE(v_sin_progresion_edss, FALSE)
    );
    
    IF v_cumple THEN
        v_estado := 'normal';
        v_justificacion := '✓ NEDA-3 CUMPLIDO: Sin evidencia de actividad de enfermedad. Los 3 criterios están cumplidos: (1) Sin recaídas, (2) Sin nuevas lesiones en RM, (3) Sin progresión de EDSS. Excelente respuesta al tratamiento.';
    ELSE
        v_estado := 'critico';
        v_justificacion := '⚠️ NEDA-3 NO CUMPLIDO: Se detectó actividad de enfermedad. Criterios no cumplidos: ';
        
        IF NOT COALESCE(v_sin_recaidas, FALSE) THEN
            v_justificacion := v_justificacion || '(1) Presencia de recaídas ';
        END IF;
        
        IF NOT COALESCE(v_sin_lesiones_rm, FALSE) THEN
            v_justificacion := v_justificacion || '(2) Nuevas lesiones en RM ';
        END IF;
        
        IF NOT COALESCE(v_sin_progresion_edss, FALSE) THEN
            v_justificacion := v_justificacion || '(3) Progresión de EDSS ';
        END IF;
        
        v_justificacion := v_justificacion || '. Requiere evaluación de eficacia terapéutica.';
    END IF;
    
    RETURN QUERY SELECT v_cumple, v_estado, v_justificacion, v_detalles;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- FUNCIÓN: obtener_metricas_ia
-- Calcula métricas de precisión de las IAs
-- =====================================================
CREATE OR REPLACE FUNCTION obtener_metricas_ia(
    p_fecha_inicio DATE DEFAULT NULL,
    p_fecha_fin DATE DEFAULT NULL
)
RETURNS TABLE(
    total_consultas BIGINT,
    selecciones_deepseek BIGINT,
    selecciones_copilot BIGINT,
    selecciones_medico BIGINT,
    accuracy_deepseek DECIMAL(5,2),
    accuracy_copilot DECIMAL(5,2)
) AS $$
DECLARE
    v_total BIGINT;
    v_deepseek BIGINT;
    v_copilot BIGINT;
    v_medico BIGINT;
    v_acc_deepseek DECIMAL(5,2);
    v_acc_copilot DECIMAL(5,2);
BEGIN
    -- Contar total de consultas
    SELECT COUNT(*)
    INTO v_total
    FROM diagnosticos_ia
    WHERE (p_fecha_inicio IS NULL OR created_at::DATE >= p_fecha_inicio)
      AND (p_fecha_fin IS NULL OR created_at::DATE <= p_fecha_fin);
    
    -- Contar selecciones por IA
    SELECT 
        COUNT(*) FILTER (WHERE ia_seleccionada = 'deepseek'),
        COUNT(*) FILTER (WHERE ia_seleccionada = 'copilot'),
        COUNT(*) FILTER (WHERE ia_seleccionada = 'medico')
    INTO v_deepseek, v_copilot, v_medico
    FROM diagnosticos_ia
    WHERE (p_fecha_inicio IS NULL OR created_at::DATE >= p_fecha_inicio)
      AND (p_fecha_fin IS NULL OR created_at::DATE <= p_fecha_fin);
    
    -- Calcular accuracy
    IF v_total > 0 THEN
        v_acc_deepseek := (v_deepseek::DECIMAL / v_total) * 100;
        v_acc_copilot := (v_copilot::DECIMAL / v_total) * 100;
    ELSE
        v_acc_deepseek := 0;
        v_acc_copilot := 0;
    END IF;
    
    RETURN QUERY SELECT v_total, v_deepseek, v_copilot, v_medico, v_acc_deepseek, v_acc_copilot;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- COMENTARIOS
-- =====================================================
COMMENT ON FUNCTION calcular_arr IS 'Calcula la Tasa Anualizada de Recaídas (ARR) para un paciente en un período';
COMMENT ON FUNCTION clasificar_t1_gd IS 'Clasifica lesiones T1 con gadolinio según rangos clínicos';
COMMENT ON FUNCTION calcular_diferencia_t2 IS 'Calcula diferencia de lesiones T2 entre estudios';
COMMENT ON FUNCTION evaluar_cdp12 IS 'Evalúa Confirmed Disability Progression a 12 semanas';
COMMENT ON FUNCTION evaluar_neda3 IS 'Evalúa cumplimiento de criterios NEDA-3';
COMMENT ON FUNCTION obtener_metricas_ia IS 'Calcula métricas de precisión de las IAs en un período';
