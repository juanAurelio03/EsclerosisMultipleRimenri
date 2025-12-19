"""
Configuración centralizada del sistema
"""
from typing import Dict, Tuple
from enum import Enum

# =====================================================
# RANGOS DE INDICADORES CLÍNICOS
# =====================================================

class IndicatorRanges:
    """Rangos de clasificación para indicadores clínicos"""
    
    ARR_RANGES = {
        'normal': (0.00, 0.09),
        'alerta': (0.10, 0.19),
        'critico': (0.20, float('inf'))
    }
    
    T1_GD_RANGES = {
        'normal': (0, 0.02),
        'alerta': (0.03, 0.49),
        'critico': (0.50, float('inf'))
    }
    
    T2_NUEVAS_RANGES = {
        'normal': (0, 0.30),
        'alerta': (0.31, 2.80),
        'critico': (2.81, float('inf'))
    }

# =====================================================
# TIPOS ENUMERADOS
# =====================================================

class TipoEM(str, Enum):
    """Tipos de Esclerosis Múltiple"""
    EMRR = "EMRR"  # Esclerosis Múltiple Remitente-Recurrente
    EMSP = "EMSP"  # Esclerosis Múltiple Secundaria Progresiva
    EMPP = "EMPP"  # Esclerosis Múltiple Primaria Progresiva

class EstadoCita(str, Enum):
    """Estados de citas"""
    PENDIENTE = "pendiente"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"

class TipoIndicador(str, Enum):
    """Tipos de indicadores clínicos"""
    ARR = "ARR"
    T1_GD = "T1_Gd"
    T2_NUEVAS = "T2_nuevas"
    CDP12 = "CDP12"
    NEDA3 = "NEDA3"

class EstadoIndicador(str, Enum):
    """Estados de clasificación de indicadores"""
    NORMAL = "normal"
    ALERTA = "alerta"
    CRITICO = "critico"

class IASeleccionada(str, Enum):
    """IA seleccionada por el médico"""
    DEEPSEEK = "deepseek"
    COPILOT = "copilot"
    MEDICO = "medico"

# =====================================================
# MENSAJES DE JUSTIFICACIÓN
# =====================================================

class JustificationMessages:
    """Plantillas de mensajes de justificación"""
    
    ARR = {
        'normal': "✓ NORMAL: ARR de {valor:.2f} está dentro del rango óptimo (<0.10). El tratamiento actual muestra buena eficacia en control de recaídas.",
        'alerta': "⚠️ ALERTA: ARR de {valor:.2f} está en rango de alerta (0.10-0.19). Requiere monitoreo cercano y evaluación de eficacia del tratamiento actual.",
        'critico': "⚠️ CRÍTICO: ARR de {valor:.2f} supera el umbral de 0.20, indicando fallo terapéutico. Se recomienda evaluar cambio de DMT o escalada terapéutica."
    }
    
    T1_GD = {
        'normal': "✓ NORMAL: {valor} lesiones T1 Gd+ detectadas (<0.03). Sin evidencia significativa de inflamación activa.",
        'alerta': "⚠️ ALERTA: {valor} lesiones T1 Gd+ detectadas (0.03-0.49). Indica actividad inflamatoria que requiere monitoreo cercano.",
        'critico': "⚠️ CRÍTICO: {valor} lesiones T1 Gd+ detectadas (≥0.50). Indica inflamación activa severa del SNC. Requiere intervención inmediata."
    }
    
    T2_NUEVAS = {
        'normal': "✓ NORMAL: {valor} nuevas lesiones T2 (≤0.30). Carga lesional estable.",
        'alerta': "⚠️ ALERTA: {valor} nuevas lesiones T2 detectadas (0.31-2.80). Requiere evaluación de eficacia terapéutica.",
        'critico': "⚠️ CRÍTICO: {valor} nuevas lesiones T2 detectadas (>2.80). Indica progresión significativa de carga lesional. Evaluar cambio de tratamiento."
    }
    
    CDP12 = {
        'normal': "✓ NORMAL: ΔEDSS = {delta:.1f}. Sin progresión de discapacidad. EDSS estable o mejorado.",
        'alerta': "⚠️ ALERTA: ΔEDSS = {delta:.1f} positivo pero no alcanza umbral CDP-12 ({umbral:.1f}). Monitorear evolución en próximas visitas.",
        'critico': "⚠️ CRÍTICO: CDP-12 confirmado. ΔEDSS = {delta:.1f} (umbral: {umbral:.1f} para EDSS basal {basal:.1f}). Progresión de discapacidad confirmada. Requiere revisión urgente del plan terapéutico."
    }
    
    NEDA3 = {
        'normal': "✓ NEDA-3 CUMPLIDO: Sin evidencia de actividad de enfermedad. Los 3 criterios están cumplidos: (1) Sin recaídas, (2) Sin nuevas lesiones en RM, (3) Sin progresión de EDSS. Excelente respuesta al tratamiento.",
        'critico': "⚠️ NEDA-3 NO CUMPLIDO: Se detectó actividad de enfermedad. {detalles}. Requiere evaluación de eficacia terapéutica."
    }

# =====================================================
# CONFIGURACIÓN DE IAs
# =====================================================

class AIConfig:
    """Configuración de APIs de IA"""
    
    DEEPSEEK_MODEL = "deepseek-chat"
    DEEPSEEK_TEMPERATURE = 0.3  # Más conservador para contexto médico
    DEEPSEEK_MAX_TOKENS = 2000
    
    COPILOT_MODEL = "gpt-4"
    COPILOT_TEMPERATURE = 0.3
    COPILOT_MAX_TOKENS = 2000
    
    # Timeout para llamadas a APIs (segundos)
    API_TIMEOUT = 30
    
    # Reintentos en caso de fallo
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # segundos

# =====================================================
# CONFIGURACIÓN DE STREAMLIT
# =====================================================

class StreamlitConfig:
    """Configuración de la aplicación Streamlit"""
    
    PAGE_TITLE = "Sistema de Gestión de Esclerosis Múltiple"
    PAGE_ICON = "🧠"
    LAYOUT = "wide"
    
    # Tema de colores
    PRIMARY_COLOR = "#1f77b4"
    BACKGROUND_COLOR = "#ffffff"
    SECONDARY_BACKGROUND_COLOR = "#f0f2f6"
    TEXT_COLOR = "#262730"
    
    # Colores de estado
    COLOR_NORMAL = "#28a745"  # Verde
    COLOR_ALERTA = "#ffc107"  # Amarillo
    COLOR_CRITICO = "#dc3545"  # Rojo

# =====================================================
# CONSTANTES DEL SISTEMA
# =====================================================

class SystemConstants:
    """Constantes generales del sistema"""
    
    # Intervalos de citas sugeridos (en meses)
    INTERVALOS_CITAS = [3, 6, 12]
    
    # Rango válido de EDSS
    EDSS_MIN = 0.0
    EDSS_MAX = 10.0
    EDSS_STEP = 0.5
    
    # Umbral para CDP-12
    CDP12_UMBRAL_BAJO = 1.0  # Para EDSS basal ≤ 5.5
    CDP12_UMBRAL_ALTO = 0.5  # Para EDSS basal > 5.5
    CDP12_EDSS_THRESHOLD = 5.5
    
    # Formato de fechas
    DATE_FORMAT = "%Y-%m-%d"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # Paginación
    ITEMS_PER_PAGE = 20

# =====================================================
# PROMPT TEMPLATES PARA IAs
# =====================================================

MEDICAL_PROMPT_TEMPLATE = """Eres un neurólogo experto en Esclerosis Múltiple con más de 20 años de experiencia clínica y de investigación.

CONTEXTO DEL PACIENTE:
- Edad: {edad} años, Sexo: {genero}
- Tipo de EM: {tipo_em}
- Años desde diagnóstico: {anos_diagnostico}
- Tratamiento actual: {tratamiento_actual}
- EDSS basal: {edss_basal} → EDSS actual: {edss_actual}

INDICADORES CLÍNICOS ACTUALES:
{indicadores_resumen}

HISTORIAL DE EVOLUCIÓN:
{historial_evolucional}

CONTEXTO CIENTÍFICO ADICIONAL:
{contexto_pdf}

SOLICITUD:
Proporciona un diagnóstico estructurado y detallado que incluya:

1. **Evaluación de Eficacia Terapéutica Actual**
   - Análisis de la respuesta al tratamiento actual
   - Identificación de signos de fallo terapéutico o respuesta subóptima

2. **Riesgo de Progresión**
   - Evaluación del riesgo de progresión de discapacidad
   - Factores de riesgo identificados
   - Pronóstico a corto y mediano plazo

3. **Recomendaciones de Manejo**
   - Mantener tratamiento actual
   - Ajustar dosis o frecuencia
   - Cambiar a otro DMT (especificar opciones)
   - Terapia de escalada si es necesario

4. **Estudios Adicionales Sugeridos**
   - Resonancia magnética de seguimiento
   - Análisis de laboratorio específicos
   - Evaluaciones funcionales
   - Otros estudios relevantes

5. **Nivel de Confianza del Diagnóstico**
   - Proporciona un número del 1 al 10
   - Justifica brevemente tu nivel de confianza

IMPORTANTE: 
- Basa tu análisis en evidencia científica actual
- Considera las guías clínicas internacionales
- Sé específico en tus recomendaciones
- Indica claramente cualquier limitación en tu evaluación

Formato de respuesta: Proporciona tu análisis en formato markdown estructurado.
"""

# =====================================================
# CONFIGURACIÓN DE LOGGING
# =====================================================

class LogConfig:
    """Configuración de logging"""
    
    LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    LOG_LEVEL = "INFO"
    LOG_FILE = "logs/app.log"
    LOG_ROTATION = "10 MB"
    LOG_RETENTION = "30 days"
