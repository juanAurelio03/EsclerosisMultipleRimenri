"""
Aplicación principal de Streamlit
Sistema de Gestión de Esclerosis Múltiple
Versión con navegación horizontal inferior
"""
import streamlit as st
from loguru import logger
import sys
from pathlib import Path

# Agregar el directorio raíz al path para imports
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from config import StreamlitConfig

# Configuración de logging
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO"
)

# Configuración de la página
st.set_page_config(
    page_title=StreamlitConfig.PAGE_TITLE,
    page_icon=StreamlitConfig.PAGE_ICON,
    layout=StreamlitConfig.LAYOUT,
    initial_sidebar_state="collapsed"  # Ocultar sidebar por defecto
)

# CSS personalizado para mejorar la apariencia Y NAVEGACIÓN INFERIOR
st.markdown("""
<style>
    /* Ocultar el sidebar completamente */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Ajustar el margen del contenido principal */
    .main .block-container {
        padding-bottom: 120px !important;
    }
    
    /* Estilos para la barra de navegación inferior */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 8px 10px 10px 10px;
        box-shadow: 0 -4px 12px rgba(0,0,0,0.15);
        z-index: 999;
        display: flex;
        justify-content: space-around;
        align-items: center;
        gap: 5px;
    }
    
    .nav-button {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: none;
        padding: 10px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 4px;
        backdrop-filter: blur(10px);
        min-width: 70px;
        flex: 1;
        max-width: 90px;
    }
    
    .nav-button .icon {
        font-size: 24px;
        line-height: 1;
    }
    
    .nav-button .label {
        font-size: 11px;
        line-height: 1.2;
        text-align: center;
    }
    
    .nav-button:hover {
        background-color: rgba(255, 255, 255, 0.25);
        transform: translateY(-3px);
    }
    
    .nav-button.active {
        background-color: white;
        color: #667eea;
        font-weight: bold;
    }
    
    /* Responsive para móviles */
    @media (max-width: 768px) {
        .bottom-nav {
            padding: 6px 5px 8px 5px;
        }
        
        .nav-button {
            min-width: 60px;
            max-width: 75px;
            padding: 8px 5px;
        }
        
        .nav-button .icon {
            font-size: 22px;
        }
        
        .nav-button .label {
            font-size: 10px;
        }
    }
    
    /* Estilos para indicadores */
    .indicator-normal {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    
    .indicator-alerta {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    
    .indicator-critico {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    
    /* Estilos para métricas */
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    /* Estilos para tablas */
    .dataframe {
        font-size: 14px;
    }
    
    /* Título principal */
    .main-title {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Subtítulos */
    .section-title {
        color: #2c3e50;
        font-size: 1.8em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 5px;
    }
    
    /* Info del paciente - Mini card superior */
    .patient-info-mini {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'paciente_seleccionado' not in st.session_state:
    st.session_state.paciente_seleccionado = None

if 'cita_actual' not in st.session_state:
    st.session_state.cita_actual = None

# Información del paciente en la parte superior (compacta)
if st.session_state.paciente_seleccionado:
    paciente = st.session_state.paciente_seleccionado
    st.markdown(f"""
    <div class="patient-info-mini">
        <strong>👤 Paciente Activo:</strong> {paciente.get('nombre_completo', 'N/A')} | 
        <strong>Edad:</strong> {paciente.get('edad', 'N/A')} | 
        <strong>Tipo EM:</strong> {paciente.get('tipo_em', 'N/A')} | 
        <strong>EDSS:</strong> {paciente.get('edss_basal', 'N/A')}
        {f" | <strong>📅 Cita:</strong> Visita #{st.session_state.cita_actual.get('numero_visita', 'N/A')}" if st.session_state.cita_actual else ""}
    </div>
    """, unsafe_allow_html=True)

# Barra de navegación superior fija y mejorada
st.markdown("""
<style>
    /* Contenedor de navegación sticky */
    .element-container:has(.bottom-nav-container) {
        position: sticky;
        top: 0;
        z-index: 999;
        background: white;
        padding: 10px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        margin-bottom: 20px;
    }
    
    .bottom-nav-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 12px 8px;
        border-radius: 15px;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .bottom-nav-container .stColumns {
        gap: 8px !important;
    }
    
    /* Estilos de botones - Desktop */
    .bottom-nav-container button {
        height: 65px !important;
        font-size: 13px !important;
        border-radius: 12px !important;
        border: none !important;
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    .bottom-nav-container button:hover {
        background-color: rgba(255, 255, 255, 0.25) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    
    .bottom-nav-container button[kind="primary"] {
        background-color: white !important;
        color: #667eea !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(255,255,255,0.3) !important;
    }
    
    .bottom-nav-container button[kind="primary"]:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 6px 20px rgba(255,255,255,0.4) !important;
    }
    
    /* Responsive para móviles - Botones más grandes */
    @media (max-width: 768px) {
        .bottom-nav-container {
            padding: 15px 5px;
            border-radius: 12px;
        }
        
        .bottom-nav-container button {
            height: 75px !important;
            font-size: 14px !important;
            padding: 10px 5px !important;
        }
        
        .bottom-nav-container .stColumns {
            gap: 6px !important;
        }
    }
    
    /* Extra pequeño - Teléfonos */
    @media (max-width: 480px) {
        .bottom-nav-container button {
            height: 70px !important;
            font-size: 12px !important;
        }
    }
</style>

<div class="bottom-nav-container">
""", unsafe_allow_html=True)


col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("🏠\nInicio", use_container_width=True, type="primary", key="nav_home"):
        st.switch_page("app.py")

with col2:
    if st.button("📋\nPacientes", use_container_width=True, key="nav_patients"):
        st.switch_page("pages/1_📋_Gestión_de_Pacientes.py")

with col3:
    if st.button("📅\nCitas", use_container_width=True, key="nav_appointments"):
        st.switch_page("pages/2_📅_Sistema_de_Citas.py")

with col4:
    if st.button("🔬\nIndicadores", use_container_width=True, key="nav_indicators"):
        st.switch_page("pages/3_🔬_Indicadores_Clínicos.py")

with col5:
    if st.button("🤖\nIA", use_container_width=True, key="nav_ai"):
        st.switch_page("pages/4_🤖_Consulta_IA.py")

with col6:
    if st.button("📊\nDashboard", use_container_width=True, key="nav_dashboard"):
        st.switch_page("pages/5_📊_Dashboard_Analítico.py")

st.markdown('</div>', unsafe_allow_html=True)

# Página principal
st.markdown('<div class="main-title">🧠 Sistema de Gestión de Esclerosis Múltiple</div>', unsafe_allow_html=True)

st.markdown("""
### Bienvenido al Sistema Integral de Gestión y Diagnóstico Asistido

Este sistema está diseñado para neurólogos y médicos especialistas en el tratamiento de **Esclerosis Múltiple (EM)**.

#### 🎯 Funcionalidades Principales:

1. **📋 Gestión de Pacientes**
   - Registro completo de pacientes con historial médico
   - Seguimiento de tipo de EM, EDSS basal y tratamiento actual

2. **📅 Sistema de Citas Progresivas**
   - Programación de citas de seguimiento (3, 6, 12 meses)
   - Tracking de evolución por visita

3. **🔬 Indicadores Clínicos**
   - **ARR** (Tasa Anualizada de Recaídas)
   - **Lesiones T1 Gd+** (Inflamación activa)
   - **Lesiones T2** (Carga lesional)
   - **CDP-12** (Progresión de discapacidad)
   - **NEDA-3** (Libertad de enfermedad)
   - Cálculo automático y clasificación por semáforo (🟢 Normal, 🟡 Alerta, 🔴 Crítico)

4. **🤖 Consulta Dual a IA**
   - Diagnóstico asistido por **DeepSeek** y **Microsoft Copilot**
   - Comparación lado a lado de recomendaciones
   - Selección médica del diagnóstico más apropiado

5. **📊 Dashboard Analítico**
   - Gráficos de evolución temporal
   - Análisis de eficacia terapéutica
   - Métricas de precisión de las IAs

6. **📄 Contexto Científico**
   - Carga de artículos científicos en PDF
   - Integración del contenido en diagnósticos de IA

---

### 🚀 Comenzar

Para empezar a usar el sistema:

1. **Selecciona o crea un paciente** en la sección de Gestión de Pacientes
2. **Programa una cita** para el seguimiento
3. **Registra los indicadores clínicos** en cada visita
4. **Consulta a las IAs** para obtener recomendaciones diagnósticas
5. **Analiza la evolución** en el dashboard

---

### 📊 Estadísticas del Sistema
""")

# Mostrar estadísticas generales
try:
    from src.database import db
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pacientes = db.listar_pacientes(activos_solo=True)
        st.metric("👥 Pacientes Activos", len(pacientes))
    
    with col2:
        # Contar citas pendientes
        citas_pendientes = db.obtener_citas_pendientes(dias_adelante=30)
        st.metric("📅 Citas Próximas (30d)", len(citas_pendientes))
    
    with col3:
        st.metric("🤖 IAs Integradas", "2")
    
    with col4:
        # Obtener métricas de IA
        try:
            metricas = db.calcular_metricas_ia()
            total_consultas = metricas.get('total_consultas', 0)
            st.metric("💬 Consultas IA", total_consultas)
        except:
            st.metric("💬 Consultas IA", "0")

except Exception as e:
    st.error(f"Error al cargar estadísticas: {e}")
    logger.error(f"Error en página principal: {e}")

st.markdown("---")



with st.expander("📖 Guía Rápida de Uso"):
    st.markdown("""
    ### Flujo de Trabajo Típico:
    
    1. **Inicio de Sesión y Selección de Paciente**
       - Navega a "Gestión de Pacientes"
       - Selecciona un paciente existente o crea uno nuevo
    
    2. **Creación de Cita**
       - Ve a "Sistema de Citas"
       - Programa una nueva cita de seguimiento
       - El sistema sugiere intervalos (3, 6, 12 meses)
    
    3. **Registro de Indicadores**
       - En "Indicadores Clínicos", selecciona la cita activa
       - Ingresa los datos clínicos (recaídas, RM, EDSS)
       - El sistema calcula automáticamente los indicadores
       - Revisa la clasificación por semáforo
    
    4. **Consulta a IAs**
       - En "Consulta IA", haz clic en "Consultar a la IA"
       - Espera las respuestas de DeepSeek y Copilot
       - Compara ambos diagnósticos
       - Selecciona el más apropiado o escribe el tuyo
    
    5. **Análisis de Evolución**
       - En "Dashboard Analítico", revisa gráficos de evolución
       - Analiza tendencias de indicadores
       - Evalúa eficacia del tratamiento actual
    """)

logger.info("Página principal cargada correctamente")