-- =====================================================
-- DATOS DE PRUEBA PARA EL SISTEMA DE GESTIÓN DE EM
-- 10 pacientes ficticios con historial completo
-- =====================================================

-- Paciente 1: María González (EMRR - Estable)
INSERT INTO pacientes (nombre_completo, edad, genero, tipo_em, edss_basal, tratamiento_actual, fecha_diagnostico, historial_medico)
VALUES (
    'María González Pérez',
    35,
    'Femenino',
    'EMRR',
    2.0,
    'Interferón beta-1a',
    '2020-03-15',
    '{"antecedentes": "Primera manifestación: neuritis óptica. Sin comorbilidades significativas.", "alergias": "Ninguna conocida"}'::jsonb
);

-- Paciente 2: Carlos Rodríguez (EMRR - Con actividad)
INSERT INTO pacientes (nombre_completo, edad, genero, tipo_em, edss_basal, tratamiento_actual, fecha_diagnostico, historial_medico)
VALUES (
    'Carlos Rodríguez Silva',
    42,
    'Masculino',
    'EMRR',
    3.5,
    'Fingolimod',
    '2018-07-22',
    '{"antecedentes": "Múltiples recaídas en primeros 2 años. Hipertensión controlada.", "alergias": "Penicilina"}'::jsonb
);

-- Paciente 3: Ana Martínez (EMSP - Progresiva)
INSERT INTO pacientes (nombre_completo, edad, genero, tipo_em, edss_basal, tratamiento_actual, fecha_diagnostico, historial_medico)
VALUES (
    'Ana Martínez López',
    48,
    'Femenino',
    'EMSP',
    6.0,
    'Ocrelizumab',
    '2015-11-08',
    '{"antecedentes": "Transición a EMSP en 2022. Requiere bastón para caminar.", "alergias": "Ninguna"}'::jsonb
);

-- Paciente 4: Jorge Fernández (EMRR - Buen control)
INSERT INTO pacientes (nombre_completo, edad, genero, tipo_em, edss_basal, tratamiento_actual, fecha_diagnostico, historial_medico)
VALUES (
    'Jorge Fernández Castro',
    38,
    'Masculino',
    'EMRR',
    1.5,
    'Natalizumab',
    '2021-02-10',
    '{"antecedentes": "Diagnóstico temprano. Excelente respuesta al tratamiento.", "alergias": "Ninguna"}'::jsonb
);

-- Paciente 5: Laura Sánchez (EMRR - Moderada)
INSERT INTO pacientes (nombre_completo, edad, genero, tipo_em, edss_basal, tratamiento_actual, fecha_diagnostico, historial_medico)
VALUES (
    'Laura Sánchez Ruiz',
    31,
    'Femenino',
    'EMRR',
    2.5,
    'Dimetilfumarato',
    '2019-09-18',
    '{"antecedentes": "Síntomas iniciales: parestesias y fatiga. Diabetes tipo 2.", "alergias": "Látex"}'::jsonb
);

-- Paciente 6: Roberto Torres (EMPP - Primaria progresiva)
INSERT INTO pacientes (nombre_completo, edad, genero, tipo_em, edss_basal, tratamiento_actual, fecha_diagnostico, historial_medico)
VALUES (
    'Roberto Torres Méndez',
    55,
    'Masculino',
    'EMPP',
    5.5,
    'Ocrelizumab',
    '2017-04-25',
    '{"antecedentes": "Progresión lenta pero constante. Sin recaídas definidas.", "alergias": "Ninguna"}'::jsonb
);

-- Paciente 7: Patricia Ramírez (EMRR - Joven)
INSERT INTO pacientes (nombre_completo, edad, genero, tipo_em, edss_basal, tratamiento_actual, fecha_diagnostico, historial_medico)
VALUES (
    'Patricia Ramírez Vega',
    27,
    'Femenino',
    'EMRR',
    1.0,
    'Teriflunomida',
    '2023-01-12',
    '{"antecedentes": "Diagnóstico reciente. Primera recaída: diplopía.", "alergias": "Ninguna"}'::jsonb
);

-- Paciente 8: Miguel Herrera (EMRR - Alta actividad)
INSERT INTO pacientes (nombre_completo, edad, genero, tipo_em, edss_basal, tratamiento_actual, fecha_diagnostico, historial_medico)
VALUES (
    'Miguel Herrera Ortiz',
    45,
    'Masculino',
    'EMRR',
    4.0,
    'Alemtuzumab',
    '2016-08-30',
    '{"antecedentes": "Alta actividad inflamatoria. Cambio reciente de tratamiento.", "alergias": "Contraste yodado"}'::jsonb
);

-- Paciente 9: Carmen Díaz (EMSP - Moderada)
INSERT INTO pacientes (nombre_completo, edad, genero, tipo_em, edss_basal, tratamiento_actual, fecha_diagnostico, historial_medico)
VALUES (
    'Carmen Díaz Morales',
    52,
    'Femenino',
    'EMSP',
    5.0,
    'Siponimod',
    '2014-06-17',
    '{"antecedentes": "Transición a EMSP en 2020. Fatiga severa.", "alergias": "Ninguna"}'::jsonb
);

-- Paciente 10: David Moreno (EMRR - Estable)
INSERT INTO pacientes (nombre_completo, edad, genero, tipo_em, edss_basal, tratamiento_actual, fecha_diagnostico, historial_medico)
VALUES (
    'David Moreno Cruz',
    40,
    'Masculino',
    'EMRR',
    2.0,
    'Glatiramer acetato',
    '2019-12-05',
    '{"antecedentes": "Buena tolerancia al tratamiento. Sin recaídas en último año.", "alergias": "Ninguna"}'::jsonb
);

-- Nota: Los IDs se generarán automáticamente
-- Para crear citas y datos adicionales, ejecuta este script después
-- y utiliza los IDs generados para crear el historial completo
