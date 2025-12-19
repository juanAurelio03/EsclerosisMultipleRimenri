# Sistema de Gestión y Diagnóstico de Esclerosis Múltiple

Sistema integral de gestión clínica y diagnóstico asistido por IA para el tratamiento de Esclerosis Múltiple (EM), dirigido a neurólogos y médicos especialistas.

## 🎯 Características Principales

- **Gestión Completa de Pacientes**: Registro y seguimiento de pacientes con EM
- **Sistema de Citas Progresivas**: Programación y tracking de visitas de seguimiento
- **Indicadores Clínicos Automatizados**: Cálculo automático de ARR, EDSS, NEDA-3, CDP-12, y lesiones RM
- **Diagnóstico Asistido por IA Dual**: Consultas paralelas a DeepSeek y Microsoft Copilot
- **Dashboard Analítico**: Visualización de evolución y métricas de precisión de IAs
- **Integración de Contexto Científico**: Carga de PDFs para mejorar diagnósticos de IA

## 🛠️ Stack Tecnológico

- **Frontend**: Streamlit
- **Backend/Base de Datos**: Supabase (PostgreSQL)
- **IA**: DeepSeek API + Microsoft Copilot API
- **Procesamiento de PDF**: PyPDF2 + pdfplumber
- **Visualización**: Plotly
- **Automatización**: n8n (opcional)

## 📋 Requisitos Previos

- Python 3.9 o superior
- Cuenta de Supabase (gratuita disponible)
- API Keys de DeepSeek y Microsoft Copilot
- Git (para clonar el repositorio)

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd proyecto_rimenri
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Copia el archivo `.env.example` a `.env` y completa las variables:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edita `.env` con tus credenciales:

```env
# Supabase Configuration
SUPABASE_URL=tu_url_de_supabase
SUPABASE_KEY=tu_clave_anonima
SUPABASE_SERVICE_KEY=tu_clave_de_servicio

# DeepSeek API
DEEPSEEK_API_KEY=tu_api_key_deepseek

# Microsoft Copilot API
COPILOT_API_KEY=tu_api_key_copilot
COPILOT_API_ENDPOINT=tu_endpoint_copilot
```

### 5. Configurar Base de Datos en Supabase

1. Crea un proyecto en [Supabase](https://supabase.com)
2. Ve al SQL Editor en tu proyecto
3. Ejecuta los scripts en este orden:
   - `database/schema.sql`
   - `database/functions.sql`
   - `database/rls_policies.sql`

### 6. Ejecutar la Aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

## 📖 Guía de Uso

### Flujo de Trabajo Típico

1. **Gestión de Pacientes** (📋)
   - Selecciona un paciente existente o crea uno nuevo
   - Completa datos demográficos y clínicos
   - Establece como paciente activo

2. **Sistema de Citas** (📅)
   - Programa una nueva cita de seguimiento
   - El sistema sugiere intervalos (3, 6, 12 meses)
   - Establece la cita como activa

3. **Indicadores Clínicos** (🔬)
   - Ingresa datos de recaídas, RM y EDSS
   - El sistema calcula automáticamente:
     - ARR (Tasa Anualizada de Recaídas)
     - Lesiones T1 Gd+ y T2
     - CDP-12 (Progresión de Discapacidad)
     - NEDA-3 (Libertad de Enfermedad)
   - Visualiza clasificación por semáforo (🟢🟡🔴)

4. **Consulta IA** (🤖)
   - Haz clic en "Consultar a las IAs"
   - Compara diagnósticos de DeepSeek y Copilot
   - Selecciona el más apropiado o escribe el tuyo

5. **Dashboard Analítico** (📊)
   - Visualiza evolución temporal de indicadores
   - Analiza cumplimiento NEDA-3
   - Revisa métricas de precisión de IAs

6. **Gestión de PDF** (📄)
   - Carga artículos científicos de referencia
   - El contenido se incluye automáticamente en consultas a IAs

## 📊 Indicadores Clínicos

### ARR (Tasa Anualizada de Recaídas)
- **Normal**: 0.00 - 0.09
- **Alerta**: 0.10 - 0.19
- **Crítico**: ≥ 0.20

### Lesiones T1 Gd+
- **Normal**: 0 - 0.02
- **Alerta**: 0.03 - 0.49
- **Crítico**: ≥ 0.50

### Lesiones T2 Nuevas
- **Normal**: 0 - 0.30
- **Alerta**: 0.31 - 2.80
- **Crítico**: > 2.80

### CDP-12 (Confirmed Disability Progression)
- Umbral: 1.0 (EDSS basal ≤5.5) o 0.5 (EDSS basal >5.5)

### NEDA-3
- Cumple si: Sin recaídas + Sin lesiones RM + Sin progresión EDSS

## 🔒 Seguridad y Compliance

- ✅ **HIPAA/GDPR Compliant**: Encriptación end-to-end
- ✅ **Row Level Security**: Control de acceso basado en roles
- ✅ **Auditoría Completa**: Log de todos los cambios
- ✅ **Datos Anonimizables**: Exportación para investigación

## 📁 Estructura del Proyecto

```
proyecto_rimenri/
├── app.py                      # Aplicación principal Streamlit
├── config.py                   # Configuración centralizada
├── requirements.txt            # Dependencias Python
├── .env.example               # Template de variables de entorno
├── database/
│   ├── schema.sql             # Esquema de base de datos
│   ├── functions.sql          # Funciones PostgreSQL
│   └── rls_policies.sql       # Políticas de seguridad
├── src/
│   ├── database/
│   │   └── supabase_client.py # Cliente de Supabase
│   ├── models/
│   │   └── patient.py         # Modelos Pydantic
│   ├── calculators/
│   │   └── clinical_indicators.py # Motor de cálculo
│   ├── ai/
│   │   ├── deepseek_client.py
│   │   ├── copilot_client.py
│   │   ├── prompt_builder.py
│   │   └── dual_consultation.py
│   └── utils/
│       └── pdf_processor.py   # Procesador de PDFs
└── pages/
    ├── 1_📋_Gestión_de_Pacientes.py
    ├── 2_📅_Sistema_de_Citas.py
    ├── 3_🔬_Indicadores_Clínicos.py
    ├── 4_🤖_Consulta_IA.py
    ├── 5_📊_Dashboard_Analítico.py
    └── 6_📄_Gestión_de_PDF.py
```

## 🧪 Testing

Para ejecutar tests (cuando estén disponibles):

```bash
pytest tests/
```

## 🤝 Contribuciones

Este es un proyecto académico. Para contribuciones, contacta al equipo de desarrollo.

## 📝 Licencia

Proyecto académico - Universidad Nacional de Trujillo

## 👥 Autores

Desarrollado para el curso de Business Intelligence - Ciclo 8

## 📞 Soporte

Para soporte técnico o preguntas, contacta al administrador del sistema.

## 🔄 Actualizaciones Futuras

- [ ] Integración con n8n para automatizaciones
- [ ] Exportación de reportes en PDF
- [ ] Notificaciones por email/SMS
- [ ] Módulo de investigación con datos anonimizados
- [ ] Integración con sistemas hospitalarios (HL7/FHIR)

## ⚠️ Notas Importantes

- Este sistema es una herramienta de apoyo diagnóstico, no reemplaza el criterio médico
- Las recomendaciones de las IAs deben ser validadas por profesionales de la salud
- Mantén las API keys seguras y nunca las compartas
- Realiza backups regulares de la base de datos

---

**Versión**: 1.0.0  
**Última Actualización**: 2025-11-28
