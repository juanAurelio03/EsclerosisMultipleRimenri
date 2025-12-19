"""
Página de Gestión de Pacientes
"""
import streamlit as st
from datetime import date
from decimal import Decimal
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.database import db
from config import TipoEM, SystemConstants
from loguru import logger

st.set_page_config(page_title="Gestión de Pacientes", page_icon="📋", layout="wide", initial_sidebar_state="collapsed")

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

# Información del paciente en la parte superior (compacta)
if st.session_state.get('paciente_seleccionado'):
    paciente = st.session_state.paciente_seleccionado
    st.markdown(f"""
    <div class="patient-info-mini">
        <strong>👤 Paciente Activo:</strong> {paciente.get('nombre_completo', 'N/A')} | 
        <strong>Edad:</strong> {paciente.get('edad', 'N/A')} | 
        <strong>Tipo EM:</strong> {paciente.get('tipo_em', 'N/A')} | 
        <strong>EDSS:</strong> {paciente.get('edss_basal', 'N/A')}
        {f" | <strong>📅 Cita:</strong> Visita #{st.session_state.cita_actual.get('numero_visita', 'N/A')}" if st.session_state.get('cita_actual') else ""}
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
    if st.button("🏠\nInicio", use_container_width=True, key="nav_home"):
        st.switch_page("app.py")

with col2:
    if st.button("📋\nPacientes", use_container_width=True, type="primary", key="nav_patients"):
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

st.markdown('<div class="section-title">📋 Gestión de Pacientes</div>', unsafe_allow_html=True)

# Tabs para organizar la interfaz
tab1, tab2 = st.tabs(["👤 Seleccionar Paciente", "➕ Nuevo Paciente"])

# =====================================================
# TAB 1: SELECCIONAR PACIENTE
# =====================================================
with tab1:
    st.markdown("### Seleccionar Paciente Existente")
    
    try:
        # Obtener lista de pacientes
        pacientes = db.listar_pacientes(activos_solo=True)
        
        if not pacientes:
            st.warning("No hay pacientes registrados en el sistema. Crea uno nuevo en la pestaña 'Nuevo Paciente'.")
        else:
            # Crear opciones para el selectbox
            opciones_pacientes = {
                f"{p['nombre_completo']} - {p['tipo_em']} (EDSS: {p['edss_basal']})": p
                for p in pacientes
            }
            
            # Selectbox para seleccionar paciente
            paciente_seleccionado_key = st.selectbox(
                "Selecciona un paciente:",
                options=list(opciones_pacientes.keys()),
                index=None,
                placeholder="Elige un paciente..."
            )
            
            if paciente_seleccionado_key:
                paciente = opciones_pacientes[paciente_seleccionado_key]
                
                # Mostrar información del paciente
                st.success(f"✅ Paciente seleccionado: **{paciente['nombre_completo']}**")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Edad", f"{paciente['edad']} años")
                
                with col2:
                    st.metric("Género", paciente['genero'])
                
                with col3:
                    st.metric("Tipo de EM", paciente['tipo_em'])
                
                with col4:
                    st.metric("EDSS Basal", paciente['edss_basal'])
                
                # Información adicional
                st.markdown("---")
                st.markdown("#### 📝 Información Clínica")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Tratamiento Actual:** {paciente.get('tratamiento_actual', 'No especificado')}")
                    st.write(f"**Fecha de Diagnóstico:** {paciente.get('fecha_diagnostico', 'N/A')}")
                
                with col2:
                    # Calcular años desde diagnóstico
                    if paciente.get('fecha_diagnostico'):
                        from dateutil import parser
                        fecha_diag = parser.parse(str(paciente['fecha_diagnostico'])).date()
                        anos_diagnostico = (date.today() - fecha_diag).days / 365.25
                        st.write(f"**Años desde Diagnóstico:** {anos_diagnostico:.1f} años")
                    
                    st.write(f"**ID del Paciente:** `{paciente['id']}`")
                
                # Historial médico
                if paciente.get('historial_medico'):
                    with st.expander("📋 Ver Historial Médico Completo"):
                        st.json(paciente['historial_medico'])
                
                # Botón para establecer como paciente activo
                st.markdown("---")
                if st.button("✅ Establecer como Paciente Activo", use_container_width=True):
                    st.session_state.paciente_seleccionado = paciente
                    st.success(f"✅ Paciente **{paciente['nombre_completo']}** establecido como activo")
                    st.balloons()
                    logger.info(f"Paciente seleccionado: {paciente['id']}")
                    
                # Estadísticas del paciente
                st.markdown("---")
                st.markdown("#### 📊 Estadísticas del Paciente")
                
                try:
                    citas = db.listar_citas_paciente(paciente['id'])
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total de Citas", len(citas))
                    
                    with col2:
                        citas_completadas = [c for c in citas if c.get('estado') == 'completada']
                        st.metric("Citas Completadas", len(citas_completadas))
                    
                    with col3:
                        citas_pendientes = [c for c in citas if c.get('estado') == 'pendiente']
                        st.metric("Citas Pendientes", len(citas_pendientes))
                    
                    # Mostrar últimas citas
                    if citas:
                        with st.expander("📅 Ver Últimas Citas"):
                            import pandas as pd
                            df_citas = pd.DataFrame(citas)
                            df_citas = df_citas[['numero_visita', 'fecha_cita', 'estado', 'notas_medicas']]
                            df_citas = df_citas.sort_values('numero_visita', ascending=False).head(5)
                            st.dataframe(df_citas, use_container_width=True)
                
                except Exception as e:
                    st.error(f"Error al cargar estadísticas: {e}")
    
    except Exception as e:
        st.error(f"Error al cargar pacientes: {e}")
        logger.error(f"Error en selección de pacientes: {e}")

# =====================================================
# TAB 2: NUEVO PACIENTE
# =====================================================
with tab2:
    st.markdown("### Registrar Nuevo Paciente")
    
    with st.form("form_nuevo_paciente"):
        st.markdown("#### Datos Demográficos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nombre_completo = st.text_input(
                "Nombre Completo *",
                placeholder="Ej: Juan Pérez García"
            )
            
            edad = st.number_input(
                "Edad *",
                min_value=1,
                max_value=120,
                value=40,
                step=1
            )
        
        with col2:
            genero = st.selectbox(
                "Género *",
                options=["Masculino", "Femenino", "Otro"],
                index=None,
                placeholder="Selecciona género..."
            )
            
            fecha_diagnostico = st.date_input(
                "Fecha de Diagnóstico *",
                value=None,
                max_value=date.today()
            )
        
        st.markdown("---")
        st.markdown("#### Información Clínica")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tipo_em = st.selectbox(
                "Tipo de Esclerosis Múltiple *",
                options=[e.value for e in TipoEM],
                index=None,
                placeholder="Selecciona tipo de EM...",
                help="EMRR: Remitente-Recurrente, EMSP: Secundaria Progresiva, EMPP: Primaria Progresiva"
            )
            
            edss_basal = st.select_slider(
                "EDSS Basal *",
                options=[i * 0.5 for i in range(21)],  # 0.0 a 10.0 en pasos de 0.5
                value=2.0,
                help="Expanded Disability Status Scale (0-10)"
            )
        
        with col2:
            tratamiento_actual = st.text_input(
                "Tratamiento Actual (DMT)",
                placeholder="Ej: Interferón beta-1a, Fingolimod, etc."
            )
            
            # Espacio para alineación
            st.write("")
        
        st.markdown("---")
        st.markdown("#### Historial Médico")
        
        historial_medico = st.text_area(
            "Antecedentes Clínicos",
            placeholder="Ingrese antecedentes médicos relevantes, comorbilidades, alergias, etc.",
            height=150
        )
        
        # Botón de envío
        st.markdown("---")
        submitted = st.form_submit_button("✅ Crear Paciente", use_container_width=True)
        
        if submitted:
            # Validar campos requeridos
            errores = []
            
            if not nombre_completo:
                errores.append("El nombre completo es requerido")
            if not genero:
                errores.append("El género es requerido")
            if not fecha_diagnostico:
                errores.append("La fecha de diagnóstico es requerida")
            if not tipo_em:
                errores.append("El tipo de EM es requerido")
            
            if errores:
                for error in errores:
                    st.error(f"❌ {error}")
            else:
                try:
                    # Preparar datos del paciente
                    datos_paciente = {
                        'nombre_completo': nombre_completo,
                        'edad': edad,
                        'genero': genero,
                        'tipo_em': tipo_em,
                        'edss_basal': float(edss_basal),
                        'tratamiento_actual': tratamiento_actual if tratamiento_actual else None,
                        'fecha_diagnostico': fecha_diagnostico.isoformat(),
                        'historial_medico': {
                            'antecedentes': historial_medico if historial_medico else ""
                        },
                        'activo': True
                    }
                    
                    # Crear paciente en la base de datos
                    nuevo_paciente = db.crear_paciente(datos_paciente)
                    
                    st.success(f"✅ Paciente **{nombre_completo}** creado exitosamente!")
                    st.info(f"ID del paciente: `{nuevo_paciente.get('id')}`")
                    st.balloons()
                    
                    # Establecer automáticamente como paciente activo
                    st.session_state.paciente_seleccionado = nuevo_paciente
                    
                    logger.info(f"Nuevo paciente creado: {nuevo_paciente.get('id')}")
                    
                    # Recargar la página para mostrar el paciente activo
                    st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Error al crear paciente: {e}")
                    logger.error(f"Error al crear paciente: {e}")

# Información del paciente activo en sidebar
if st.session_state.get('paciente_seleccionado'):
    st.sidebar.success("✅ Paciente activo establecido")
    st.sidebar.write(f"**{st.session_state.paciente_seleccionado.get('nombre_completo')}**")
