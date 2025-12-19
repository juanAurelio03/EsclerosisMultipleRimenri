-- =====================================================
-- DATOS DE PRUEBA PARA SISTEMA DE ESCLEROSIS MÚLTIPLE
-- Ejecutar DESPUÉS de init_database.sql
-- =====================================================

-- =====================================================
-- INSERTAR PACIENTES
-- =====================================================

INSERT INTO pacientes (nombre_completo, edad, genero, tipo_em, edss_basal, tratamiento_actual, fecha_diagnostico, historial_medico, activo) VALUES
('María González Pérez', 34, 'Femenino', 'EMRR', 2.0, 'Interferón beta-1a', '2020-03-15', '{"antecedentes": "Sin comorbilidades previas", "alergias": "Ninguna"}', true),
('Juan Carlos Rodríguez', 42, 'Masculino', 'EMSP', 4.5, 'Fingolimod', '2018-07-22', '{"antecedentes": "Hipertensión controlada", "alergias": "Penicilina"}', true),
('Ana Martínez López', 28, 'Femenino', 'EMRR', 1.5, 'Natalizumab', '2021-11-10', '{"antecedentes": "Ninguno", "alergias": "Ninguna"}', true),
('Pedro Sánchez García', 51, 'Masculino', 'EMPP', 6.0, 'Ocrelizumab', '2015-02-28', '{"antecedentes": "Diabetes tipo 2", "alergias": "Ninguna"}', true),
('Laura Fernández Torres', 37, 'Femenino', 'EMRR', 3.0, 'Teriflunomida', '2019-09-05', '{"antecedentes": "Ninguno", "alergias": "Ninguna"}', true),
('Carlos Jiménez Ruiz', 45, 'Masculino', 'EMSP', 5.5, 'Siponimod', '2017-04-18', '{"antecedentes": "Dislipidemia", "alergias": "Ninguna"}', true),
('Isabel Moreno Díaz', 31, 'Femenino', 'EMRR', 2.5, 'Dimetilfumarato', '2020-12-03', '{"antecedentes": "Ninguno", "alergias": "Ninguna"}', true),
('Miguel Ángel Romero', 48, 'Masculino', 'EMRR', 3.5, 'Alemtuzumab', '2018-06-14', '{"antecedentes": "Ninguno", "alergias": "Ninguna"}', true),
('Carmen Navarro Silva', 39, 'Femenino', 'EMSP', 4.0, 'Cladribina', '2019-01-25', '{"antecedentes": "Hipotiroidismo", "alergias": "Ninguna"}', true),
('Francisco López Martín', 55, 'Masculino', 'EMPP', 7.0, 'Ocrelizumab', '2014-08-30', '{"antecedentes": "Ninguno", "alergias": "Sulfamidas"}', true),
('Sofía Ramírez Ortiz', 29, 'Femenino', 'EMRR', 1.0, 'Interferón beta-1b', '2022-02-14', '{"antecedentes": "Ninguno", "alergias": "Ninguna"}', true),
('Diego Torres Vega', 43, 'Masculino', 'EMRR', 2.5, 'Glatiramer', '2019-05-20', '{"antecedentes": "Ninguno", "alergias": "Ninguna"}', true);

-- =====================================================
-- INSERTAR CITAS
-- =====================================================

-- Citas para María González Pérez (primer paciente)
INSERT INTO citas (paciente_id, fecha_cita, numero_visita, estado, notas_medicas)
SELECT id, '2023-06-15 10:00:00+00', 1, 'completada', 'Primera evaluación post-diagnóstico. Paciente estable.'
FROM pacientes WHERE nombre_completo = 'María González Pérez';

INSERT INTO citas (paciente_id, fecha_cita, numero_visita, estado, notas_medicas)
SELECT id, '2023-12-15 10:00:00+00', 2, 'completada', 'Seguimiento a 6 meses. Sin recaídas.'
FROM pacientes WHERE nombre_completo = 'María González Pérez';

INSERT INTO citas (paciente_id, fecha_cita, numero_visita, estado, notas_medicas)
SELECT id, '2024-06-15 10:00:00+00', 3, 'completada', 'Seguimiento a 12 meses. Buena respuesta al tratamiento.'
FROM pacientes WHERE nombre_completo = 'María González Pérez';

INSERT INTO citas (paciente_id, fecha_cita, numero_visita, estado, notas_medicas)
SELECT id, '2024-12-15 10:00:00+00', 4, 'pendiente', 'Próxima evaluación programada.'
FROM pacientes WHERE nombre_completo = 'María González Pérez';

-- Citas para Juan Carlos Rodríguez
INSERT INTO citas (paciente_id, fecha_cita, numero_visita, estado, notas_medicas)
SELECT id, '2023-03-22 11:00:00+00', 1, 'completada', 'Evaluación inicial. EDSS estable.'
FROM pacientes WHERE nombre_completo = 'Juan Carlos Rodríguez';

INSERT INTO citas (paciente_id, fecha_cita, numero_visita, estado, notas_medicas)
SELECT id, '2023-09-22 11:00:00+00', 2, 'completada', 'Seguimiento a 6 meses. Una recaída leve.'
FROM pacientes WHERE nombre_completo = 'Juan Carlos Rodríguez';

INSERT INTO citas (paciente_id, fecha_cita, numero_visita, estado, notas_medicas)
SELECT id, '2024-03-22 11:00:00+00', 3, 'completada', 'Seguimiento a 12 meses. Progresión leve.'
FROM pacientes WHERE nombre_completo = 'Juan Carlos Rodríguez';

-- Citas para Ana Martínez López
INSERT INTO citas (paciente_id, fecha_cita, numero_visita, estado, notas_medicas)
SELECT id, '2023-05-10 09:00:00+00', 1, 'completada', 'Primera evaluación. Paciente joven, buen pronóstico.'
FROM pacientes WHERE nombre_completo = 'Ana Martínez López';

INSERT INTO citas (paciente_id, fecha_cita, numero_visita, estado, notas_medicas)
SELECT id, '2023-11-10 09:00:00+00', 2, 'completada', 'Seguimiento a 6 meses. Sin actividad de enfermedad.'
FROM pacientes WHERE nombre_completo = 'Ana Martínez López';

INSERT INTO citas (paciente_id, fecha_cita, numero_visita, estado, notas_medicas)
SELECT id, '2024-05-10 09:00:00+00', 3, 'pendiente', 'Próxima evaluación.'
FROM pacientes WHERE nombre_completo = 'Ana Martínez López';

-- Citas para Pedro Sánchez García
INSERT INTO citas (paciente_id, fecha_cita, numero_visita, estado, notas_medicas)
SELECT id, '2023-02-28 14:00:00+00', 1, 'completada', 'Evaluación anual. Progresión lenta.'
FROM pacientes WHERE nombre_completo = 'Pedro Sánchez García';

INSERT INTO citas (paciente_id, fecha_cita, numero_visita, estado, notas_medicas)
SELECT id, '2024-02-28 14:00:00+00', 2, 'completada', 'Seguimiento anual. EDSS incrementado.'
FROM pacientes WHERE nombre_completo = 'Pedro Sánchez García';

-- Citas para Laura Fernández Torres
INSERT INTO citas (paciente_id, fecha_cita, numero_visita, estado, notas_medicas)
SELECT id, '2023-09-05 10:30:00+00', 1, 'completada', 'Evaluación de seguimiento. Estable.'
FROM pacientes WHERE nombre_completo = 'Laura Fernández Torres';

INSERT INTO citas (paciente_id, fecha_cita, numero_visita, estado, notas_medicas)
SELECT id, '2024-03-05 10:30:00+00', 2, 'completada', 'Seguimiento a 6 meses. Sin cambios significativos.'
FROM pacientes WHERE nombre_completo = 'Laura Fernández Torres';

INSERT INTO citas (paciente_id, fecha_cita, numero_visita, estado, notas_medicas)
SELECT id, '2024-09-05 10:30:00+00', 3, 'pendiente', 'Próxima evaluación.'
FROM pacientes WHERE nombre_completo = 'Laura Fernández Torres';

-- =====================================================
-- INSERTAR INDICADORES CLÍNICOS
-- =====================================================

-- Indicadores para María González - Visita 1
INSERT INTO indicadores_cita (cita_id, indicador_tipo, valor_calculado, estado, justificacion_texto, variables_entrada)
SELECT c.id, 'ARR', 0.00, 'normal', '✓ NORMAL: ARR de 0.00 está dentro del rango óptimo (<0.10). El tratamiento actual muestra buena eficacia en control de recaídas.', '{"recaidas": 0}'
FROM citas c JOIN pacientes p ON c.paciente_id = p.id
WHERE p.nombre_completo = 'María González Pérez' AND c.numero_visita = 1;

INSERT INTO indicadores_cita (cita_id, indicador_tipo, valor_calculado, estado, justificacion_texto, variables_entrada)
SELECT c.id, 'T1_Gd', 0, 'normal', '✓ NORMAL: 0 lesiones T1 Gd+ detectadas (<0.03). Sin evidencia significativa de inflamación activa.', '{"lesiones_t1_gd": 0}'
FROM citas c JOIN pacientes p ON c.paciente_id = p.id
WHERE p.nombre_completo = 'María González Pérez' AND c.numero_visita = 1;

INSERT INTO indicadores_cita (cita_id, indicador_tipo, valor_calculado, estado, justificacion_texto, variables_entrada)
SELECT c.id, 'T2_nuevas', 0, 'normal', '✓ NORMAL: 0 nuevas lesiones T2 (≤0.30). Carga lesional estable.', '{"lesiones_t2_actuales": 5, "lesiones_t2_previas": 5}'
FROM citas c JOIN pacientes p ON c.paciente_id = p.id
WHERE p.nombre_completo = 'María González Pérez' AND c.numero_visita = 1;

INSERT INTO indicadores_cita (cita_id, indicador_tipo, valor_calculado, estado, justificacion_texto, variables_entrada)
SELECT c.id, 'CDP12', 0.0, 'normal', '✓ NORMAL: ΔEDSS = 0.0. Sin progresión de discapacidad. EDSS estable o mejorado.', '{"edss_basal": 2.0, "edss_actual": 2.0, "progresion_confirmada": false}'
FROM citas c JOIN pacientes p ON c.paciente_id = p.id
WHERE p.nombre_completo = 'María González Pérez' AND c.numero_visita = 1;

INSERT INTO indicadores_cita (cita_id, indicador_tipo, valor_calculado, estado, justificacion_texto, variables_entrada)
SELECT c.id, 'NEDA3', 1.0, 'normal', '✓ NEDA-3 CUMPLIDO: Sin evidencia de actividad de enfermedad. Los 3 criterios están cumplidos: (1) Sin recaídas, (2) Sin nuevas lesiones en RM, (3) Sin progresión de EDSS. Excelente respuesta al tratamiento.', '{"sin_recaidas": true, "sin_lesiones_rm": true, "sin_progresion_edss": true}'
FROM citas c JOIN pacientes p ON c.paciente_id = p.id
WHERE p.nombre_completo = 'María González Pérez' AND c.numero_visita = 1;

-- Indicadores para Juan Carlos - Visita 2 (con recaída)
INSERT INTO indicadores_cita (cita_id, indicador_tipo, valor_calculado, estado, justificacion_texto, variables_entrada)
SELECT c.id, 'ARR', 0.15, 'alerta', '⚠️ ALERTA: ARR de 0.15 está en rango de alerta (0.10-0.19). Requiere monitoreo cercano y evaluación de eficacia del tratamiento actual.', '{"recaidas": 1}'
FROM citas c JOIN pacientes p ON c.paciente_id = p.id
WHERE p.nombre_completo = 'Juan Carlos Rodríguez' AND c.numero_visita = 2;

INSERT INTO indicadores_cita (cita_id, indicador_tipo, valor_calculado, estado, justificacion_texto, variables_entrada)
SELECT c.id, 'T1_Gd', 2, 'alerta', '⚠️ ALERTA: 2 lesiones T1 Gd+ detectadas (0.03-0.49). Indica actividad inflamatoria que requiere monitoreo cercano.', '{"lesiones_t1_gd": 2}'
FROM citas c JOIN pacientes p ON c.paciente_id = p.id
WHERE p.nombre_completo = 'Juan Carlos Rodríguez' AND c.numero_visita = 2;

INSERT INTO indicadores_cita (cita_id, indicador_tipo, valor_calculado, estado, justificacion_texto, variables_entrada)
SELECT c.id, 'T2_nuevas', 3, 'critico', '⚠️ CRÍTICO: 3 nuevas lesiones T2 detectadas (>2.80). Indica progresión significativa de carga lesional. Evaluar cambio de tratamiento.', '{"lesiones_t2_actuales": 15, "lesiones_t2_previas": 12}'
FROM citas c JOIN pacientes p ON c.paciente_id = p.id
WHERE p.nombre_completo = 'Juan Carlos Rodríguez' AND c.numero_visita = 2;

INSERT INTO indicadores_cita (cita_id, indicador_tipo, valor_calculado, estado, justificacion_texto, variables_entrada)
SELECT c.id, 'CDP12', 0.5, 'alerta', '⚠️ ALERTA: ΔEDSS = 0.5 positivo pero no alcanza umbral CDP-12 (1.0). Monitorear evolución en próximas visitas.', '{"edss_basal": 4.5, "edss_actual": 5.0, "progresion_confirmada": false}'
FROM citas c JOIN pacientes p ON c.paciente_id = p.id
WHERE p.nombre_completo = 'Juan Carlos Rodríguez' AND c.numero_visita = 2;

INSERT INTO indicadores_cita (cita_id, indicador_tipo, valor_calculado, estado, justificacion_texto, variables_entrada)
SELECT c.id, 'NEDA3', 0.0, 'critico', '⚠️ NEDA-3 NO CUMPLIDO: Se detectó actividad de enfermedad. Criterios no cumplidos: (1) Presencia de recaídas (2) Nuevas lesiones en RM . Requiere evaluación de eficacia terapéutica.', '{"sin_recaidas": false, "sin_lesiones_rm": false, "sin_progresion_edss": true}'
FROM citas c JOIN pacientes p ON c.paciente_id = p.id
WHERE p.nombre_completo = 'Juan Carlos Rodríguez' AND c.numero_visita = 2;

-- Indicadores para Ana Martínez - Visita 2 (excelente respuesta)
INSERT INTO indicadores_cita (cita_id, indicador_tipo, valor_calculado, estado, justificacion_texto, variables_entrada)
SELECT c.id, 'ARR', 0.00, 'normal', '✓ NORMAL: ARR de 0.00 está dentro del rango óptimo (<0.10). El tratamiento actual muestra buena eficacia en control de recaídas.', '{"recaidas": 0}'
FROM citas c JOIN pacientes p ON c.paciente_id = p.id
WHERE p.nombre_completo = 'Ana Martínez López' AND c.numero_visita = 2;

INSERT INTO indicadores_cita (cita_id, indicador_tipo, valor_calculado, estado, justificacion_texto, variables_entrada)
SELECT c.id, 'T1_Gd', 0, 'normal', '✓ NORMAL: 0 lesiones T1 Gd+ detectadas (<0.03). Sin evidencia significativa de inflamación activa.', '{"lesiones_t1_gd": 0}'
FROM citas c JOIN pacientes p ON c.paciente_id = p.id
WHERE p.nombre_completo = 'Ana Martínez López' AND c.numero_visita = 2;

INSERT INTO indicadores_cita (cita_id, indicador_tipo, valor_calculado, estado, justificacion_texto, variables_entrada)
SELECT c.id, 'T2_nuevas', 0, 'normal', '✓ NORMAL: 0 nuevas lesiones T2 (≤0.30). Carga lesional estable.', '{"lesiones_t2_actuales": 3, "lesiones_t2_previas": 3}'
FROM citas c JOIN pacientes p ON c.paciente_id = p.id
WHERE p.nombre_completo = 'Ana Martínez López' AND c.numero_visita = 2;

INSERT INTO indicadores_cita (cita_id, indicador_tipo, valor_calculado, estado, justificacion_texto, variables_entrada)
SELECT c.id, 'CDP12', -0.5, 'normal', '✓ NORMAL: ΔEDSS = -0.5. Sin progresión de discapacidad. EDSS estable o mejorado.', '{"edss_basal": 1.5, "edss_actual": 1.0, "progresion_confirmada": false}'
FROM citas c JOIN pacientes p ON c.paciente_id = p.id
WHERE p.nombre_completo = 'Ana Martínez López' AND c.numero_visita = 2;

INSERT INTO indicadores_cita (cita_id, indicador_tipo, valor_calculado, estado, justificacion_texto, variables_entrada)
SELECT c.id, 'NEDA3', 1.0, 'normal', '✓ NEDA-3 CUMPLIDO: Sin evidencia de actividad de enfermedad. Los 3 criterios están cumplidos: (1) Sin recaídas, (2) Sin nuevas lesiones en RM, (3) Sin progresión de EDSS. Excelente respuesta al tratamiento.', '{"sin_recaidas": true, "sin_lesiones_rm": true, "sin_progresion_edss": true}'
FROM citas c JOIN pacientes p ON c.paciente_id = p.id
WHERE p.nombre_completo = 'Ana Martínez López' AND c.numero_visita = 2;

-- =====================================================
-- INSERTAR DIAGNÓSTICOS IA (ejemplos)
-- =====================================================

INSERT INTO diagnosticos_ia (cita_id, diagnostico_deepseek, confianza_deepseek, diagnostico_copilot, confianza_copilot, ia_seleccionada)
SELECT c.id, 
    'Paciente con excelente respuesta al tratamiento con Interferón beta-1a. NEDA-3 cumplido. Recomendación: Continuar con tratamiento actual y seguimiento programado.',
    8.5,
    'Respuesta óptima al DMT actual. Sin actividad de enfermedad. Mantener régimen terapéutico y monitoreo semestral.',
    8.2,
    'deepseek'
FROM citas c JOIN pacientes p ON c.paciente_id = p.id
WHERE p.nombre_completo = 'María González Pérez' AND c.numero_visita = 1;

INSERT INTO diagnosticos_ia (cita_id, diagnostico_deepseek, confianza_deepseek, diagnostico_copilot, confianza_copilot, ia_seleccionada, diagnostico_medico_override, justificacion_medico)
SELECT c.id, 
    'Actividad de enfermedad detectada. ARR en rango de alerta y nuevas lesiones T2. Considerar escalada terapéutica a DMT de alta eficacia.',
    7.8,
    'Fallo terapéutico parcial. Presencia de recaída y actividad en RM. Evaluar cambio a Natalizumab u Ocrelizumab.',
    8.0,
    'medico',
    'Paciente presenta actividad de enfermedad a pesar de Fingolimod. Dado el perfil de riesgo y progresión, se decide cambio a Ocrelizumab. Programar evaluación pre-tratamiento.',
    'La IA sugiere correctamente escalada terapéutica, pero basado en el perfil del paciente y comorbilidades, Ocrelizumab es la mejor opción.'
FROM citas c JOIN pacientes p ON c.paciente_id = p.id
WHERE p.nombre_completo = 'Juan Carlos Rodríguez' AND c.numero_visita = 2;

-- =====================================================
-- INSERTAR MÉTRICAS IA
-- =====================================================

INSERT INTO metricas_ia (fecha_calculo, total_consultas, selecciones_deepseek, selecciones_copilot, selecciones_medico_override, accuracy_deepseek, accuracy_copilot)
VALUES
('2024-01-31', 15, 6, 5, 4, 40.00, 33.33),
('2024-02-29', 22, 9, 8, 5, 40.91, 36.36),
('2024-03-31', 18, 7, 6, 5, 38.89, 33.33),
('2024-04-30', 25, 11, 9, 5, 44.00, 36.00),
('2024-05-31', 20, 8, 7, 5, 40.00, 35.00);

-- =====================================================
-- INSERTAR DOCUMENTO DE REFERENCIA
-- =====================================================

INSERT INTO documentos_referencia (nombre_archivo, contenido_extraido, metadata, activo)
VALUES
('guia_clinica_em_2024.pdf', 
'Guía Clínica de Esclerosis Múltiple 2024. Criterios diagnósticos: Diseminación en espacio y tiempo según criterios de McDonald 2017. Tratamientos modificadores de enfermedad (DMT): Primera línea incluye Interferones, Glatiramer, Teriflunomida, Dimetilfumarato. Segunda línea: Natalizumab, Fingolimod, Alemtuzumab, Ocrelizumab, Cladribina. Indicadores de eficacia: NEDA-3 (No Evidence of Disease Activity) incluye ausencia de recaídas, ausencia de progresión de discapacidad (CDP), ausencia de actividad en RM. ARR (Annualized Relapse Rate) objetivo <0.1. EDSS (Expanded Disability Status Scale) 0-10.',
'{"autor": "Sociedad Española de Neurología", "año": 2024, "tipo": "guía_clínica"}',
true);

-- =====================================================
-- VERIFICACIÓN
-- =====================================================

-- Contar registros insertados
SELECT 'Pacientes' as tabla, COUNT(*) as total FROM pacientes
UNION ALL
SELECT 'Citas', COUNT(*) FROM citas
UNION ALL
SELECT 'Indicadores', COUNT(*) FROM indicadores_cita
UNION ALL
SELECT 'Diagnósticos IA', COUNT(*) FROM diagnosticos_ia
UNION ALL
SELECT 'Métricas IA', COUNT(*) FROM metricas_ia
UNION ALL
SELECT 'Documentos', COUNT(*) FROM documentos_referencia;
