"""
Página de Sistema de Citas
"""
import streamlit as st
from datetime import datetime, timedelta, date
import sys
from pathlib import Path
import pandas as pd

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.database import db
from config import EstadoCita, SystemConstants
from loguru import logger

st.set_page_config(page_title="Sistema de Citas", page_icon="📅", layout="wide", initial_sidebar_state="collapsed")

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
    if st.button("📋\nPacientes", use_container_width=True, key="nav_patients"):
        st.switch_page("pages/1_📋_Gestión_de_Pacientes.py")

with col3:
    if st.button("📅\nCitas", use_container_width=True, type="primary", key="nav_appointments"):
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


st.markdown('<div class="section-title">📅 Sistema de Citas Progresivas</div>', unsafe_allow_html=True)

# Verificar que hay un paciente seleccionado
if not st.session_state.get('paciente_seleccionado'):
    st.warning("⚠️ No hay paciente seleccionado. Por favor, selecciona un paciente en la página de Gestión de Pacientes.")
    st.stop()

paciente = st.session_state.paciente_seleccionado

st.info(f"**Paciente:** {paciente.get('nombre_completo')} - {paciente.get('tipo_em')}")

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 Citas del Paciente", "➕ Nueva Cita", "📅 Próximas Citas"])

# =====================================================
# TAB 1: CITAS DEL PACIENTE
# =====================================================
with tab1:
    st.markdown("### Historial de Citas")
    
    try:
        citas = db.listar_citas_paciente(paciente['id'])
        
        if not citas:
            st.info("Este paciente no tiene citas registradas. Crea una nueva cita en la pestaña 'Nueva Cita'.")
        else:
            # Filtros
            col1, col2 = st.columns(2)
            
            with col1:
                filtro_estado = st.multiselect(
                    "Filtrar por estado:",
                    options=['pendiente', 'completada', 'cancelada'],
                    default=['pendiente', 'completada']
                )
            
            # Filtrar citas
            citas_filtradas = [c for c in citas if c.get('estado') in filtro_estado]
            
            # Mostrar métricas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Citas", len(citas))
            with col2:
                completadas = len([c for c in citas if c.get('estado') == 'completada'])
                st.metric("Completadas", completadas)
            with col3:
                pendientes = len([c for c in citas if c.get('estado') == 'pendiente'])
                st.metric("Pendientes", pendientes)
            with col4:
                canceladas = len([c for c in citas if c.get('estado') == 'cancelada'])
                st.metric("Canceladas", canceladas)
            
            st.markdown("---")
            
            # Tabla de citas
            if citas_filtradas:
                df = pd.DataFrame(citas_filtradas)
                df['fecha_cita'] = pd.to_datetime(df['fecha_cita']).dt.strftime('%Y-%m-%d %H:%M')
                df_display = df[['numero_visita', 'fecha_cita', 'estado', 'notas_medicas']].copy()
                df_display.columns = ['Visita #', 'Fecha', 'Estado', 'Notas']
                df_display = df_display.sort_values('Visita #', ascending=False)
                
                st.dataframe(df_display, use_container_width=True, height=400)
                
                # Seleccionar cita para establecer como activa
                st.markdown("---")
                st.markdown("#### Establecer Cita Activa")
                
                cita_seleccionada = st.selectbox(
                    "Selecciona una cita para trabajar:",
                    options=[f"Visita #{c['numero_visita']} - {c['fecha_cita'][:10]} ({c['estado']})" for c in citas_filtradas],
                    index=None
                )
                
                if cita_seleccionada and st.button("✅ Establecer como Cita Activa"):
                    # Extraer número de visita
                    numero_visita = int(cita_seleccionada.split('#')[1].split(' -')[0])
                    cita = next(c for c in citas if c['numero_visita'] == numero_visita)
                    st.session_state.cita_actual = cita
                    st.success(f"✅ Cita Visita #{numero_visita} establecida como activa")
                    st.balloons()
            else:
                st.info("No hay citas con los filtros seleccionados.")
    
    except Exception as e:
        st.error(f"Error al cargar citas: {e}")
        logger.error(f"Error en citas del paciente: {e}")

# =====================================================
# TAB 2: NUEVA CITA
# =====================================================
with tab2:
    st.markdown("### Programar Nueva Cita")
    
    try:
        # Obtener última cita para sugerir intervalo
        citas = db.listar_citas_paciente(paciente['id'])
        ultima_cita = None
        if citas:
            citas_ordenadas = sorted(citas, key=lambda x: x.get('fecha_cita', ''), reverse=True)
            ultima_cita = citas_ordenadas[0]
        
        if ultima_cita:
            st.info(f"📌 Última cita: Visita #{ultima_cita['numero_visita']} - {ultima_cita['fecha_cita'][:10]}")
            
            # Sugerir fechas según intervalos
            ultima_fecha = datetime.fromisoformat(ultima_cita['fecha_cita'].replace('Z', '+00:00'))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                fecha_3m = ultima_fecha + timedelta(days=90)
                st.success(f"**3 meses:** {fecha_3m.strftime('%Y-%m-%d')}")
            with col2:
                fecha_6m = ultima_fecha + timedelta(days=180)
                st.success(f"**6 meses:** {fecha_6m.strftime('%Y-%m-%d')}")
            with col3:
                fecha_12m = ultima_fecha + timedelta(days=365)
                st.success(f"**12 meses:** {fecha_12m.strftime('%Y-%m-%d')}")
        
        st.markdown("---")
        
        with st.form("form_nueva_cita"):
            col1, col2 = st.columns(2)
            
            with col1:
                fecha_cita = st.date_input(
                    "Fecha de la Cita *",
                    value=date.today() + timedelta(days=7),
                    min_value=date.today()
                )
            
            with col2:
                hora_cita = st.time_input(
                    "Hora de la Cita *",
                    value=datetime.strptime("09:00", "%H:%M").time()
                )
            
            notas_medicas = st.text_area(
                "Notas Médicas (Opcional)",
                placeholder="Motivo de la cita, observaciones iniciales, etc.",
                height=100
            )
            
            submitted = st.form_submit_button("✅ Crear Cita", type="primary", use_container_width=True)
            
            if submitted:
                try:
                    # Combinar fecha y hora
                    fecha_hora = datetime.combine(fecha_cita, hora_cita)
                    
                    datos_cita = {
                        'paciente_id': paciente['id'],
                        'fecha_cita': fecha_hora.isoformat(),
                        'estado': 'pendiente',
                        'notas_medicas': notas_medicas if notas_medicas else None
                    }
                    
                    nueva_cita = db.crear_cita(datos_cita)
                    
                    st.success(f"✅ Cita creada exitosamente! Visita #{nueva_cita['numero_visita']}")
                    st.balloons()
                    
                    # Establecer automáticamente como cita activa
                    st.session_state.cita_actual = nueva_cita
                    
                    logger.info(f"Nueva cita creada: {nueva_cita['id']}")
                    
                    # Recargar la página para mostrar la cita activa
                    st.rerun()
                
                except Exception as e:
                    st.error(f"Error al crear cita: {e}")
                    logger.error(f"Error al crear cita: {e}")
    
    except Exception as e:
        st.error(f"Error: {e}")

# =====================================================
# TAB 3: PRÓXIMAS CITAS
# =====================================================
with tab3:
    st.markdown("### Próximas Citas del Sistema")
    
    try:
        dias_adelante = st.slider("Mostrar citas de los próximos:", 1, 90, 30, help="Días hacia adelante")
        
        citas_proximas = db.obtener_citas_pendientes(dias_adelante=dias_adelante)
        
        if not citas_proximas:
            st.info(f"No hay citas pendientes en los próximos {dias_adelante} días.")
        else:
            st.success(f"Se encontraron {len(citas_proximas)} citas pendientes")
            
            # Crear DataFrame
            data = []
            for cita in citas_proximas:
                paciente_cita = cita.get('pacientes', {})
                data.append({
                    'Paciente': paciente_cita.get('nombre_completo', 'N/A'),
                    'Visita #': cita.get('numero_visita'),
                    'Fecha': datetime.fromisoformat(cita['fecha_cita'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M'),
                    'Tipo EM': paciente_cita.get('tipo_em', 'N/A'),
                    'Estado': cita.get('estado')
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error al cargar próximas citas: {e}")
