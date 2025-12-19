"""
Página de Consulta Dual a IA
"""
import streamlit as st
import asyncio
import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.database import db
from src.ai import DualAIConsultation
from config import IASeleccionada
from loguru import logger

st.set_page_config(page_title="Consulta IA", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")

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
    if st.button("📅\nCitas", use_container_width=True, key="nav_appointments"):
        st.switch_page("pages/2_📅_Sistema_de_Citas.py")

with col4:
    if st.button("🔬\nIndicadores", use_container_width=True, key="nav_indicators"):
        st.switch_page("pages/3_🔬_Indicadores_Clínicos.py")

with col5:
    if st.button("🤖\nIA", use_container_width=True, type="primary", key="nav_ai"):
        st.switch_page("pages/4_🤖_Consulta_IA.py")

with col6:
    if st.button("📊\nDashboard", use_container_width=True, key="nav_dashboard"):
        st.switch_page("pages/5_📊_Dashboard_Analítico.py")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">🤖 Consulta Dual a Inteligencia Artificial</div>', unsafe_allow_html=True)

# Verificar paciente y cita
if not st.session_state.get('paciente_seleccionado'):
    st.warning("⚠️ No hay paciente seleccionado.")
    st.stop()

if not st.session_state.get('cita_actual'):
    st.warning("⚠️ No hay cita activa.")
    st.stop()

paciente = st.session_state.paciente_seleccionado
cita = st.session_state.cita_actual

st.info(f"**Paciente:** {paciente['nombre_completo']} | **Cita:** Visita #{cita['numero_visita']}")

# Verificar que hay indicadores registrados
try:
    indicadores = db.obtener_indicadores_cita(cita['id'])
    
    if not indicadores:
        st.warning("⚠️ No hay indicadores registrados para esta cita. Por favor, registra los indicadores clínicos primero.")
        st.stop()
    
    # Mostrar resumen de indicadores
    with st.expander("📊 Ver Indicadores Actuales"):
        for ind in indicadores:
            estado_emoji = {'normal': '✅', 'alerta': '⚠️', 'critico': '🔴'}[ind['estado']]
            st.write(f"{estado_emoji} **{ind['indicador_tipo']}**: {ind.get('valor_calculado', 'N/A')} - {ind['estado'].upper()}")

except Exception as e:
    st.error(f"Error al verificar indicadores: {e}")
    st.stop()

# Tabs
tab1, tab2 = st.tabs(["🤖 Consultar IAs", "📜 Historial de Diagnósticos"])

# =====================================================
# TAB 1: CONSULTAR IAs
# =====================================================
with tab1:
    st.markdown("### Diagnóstico Asistido por IA")
    
    st.info("""
    💡 **Cómo funciona:**
    1. El sistema prepara un contexto completo con el historial del paciente
    2. Se envían consultas paralelas a **DeepSeek** y **Microsoft Copilot**
    3. Ambas IAs analizan los datos y generan diagnósticos independientes
    4. Tú comparas ambos diagnósticos y seleccionas el más apropiado
    5. Opcionalmente, puedes escribir tu propio diagnóstico
    """)
    
    # Verificar si ya existe un diagnóstico
    diagnostico_existente = None
    try:
        diagnostico_existente = db.obtener_diagnostico_ia(cita['id'])
    except:
        pass
    
    if diagnostico_existente:
        st.warning("⚠️ Ya existe un diagnóstico de IA para esta cita. Puedes consultarlo en la pestaña 'Historial de Diagnósticos'.")
        
        if st.button("🔄 Generar Nuevo Diagnóstico (sobrescribirá el anterior)"):
            diagnostico_existente = None
    
    if not diagnostico_existente:
        st.markdown("---")
        
        # Botón para consultar
        if st.button("🤖 CONSULTAR A LAS IAs", type="primary", use_container_width=True):
            
            with st.spinner("🔄 Preparando contexto y consultando a las IAs... Esto puede tomar 10-30 segundos..."):
                try:
                    # Intentar usar n8n primero si está configurado
                    usar_n8n = False
                    try:
                        from src.n8n import n8n_client
                        if n8n_client.is_configured():
                            usar_n8n = True
                            st.info("🔄 Usando n8n para orquestar las consultas...")
                    except:
                        pass
                    
                    # Si n8n está configurado, usarlo
                    if usar_n8n:
                        from src.n8n import n8n_client
                        
                        # Preparar prompt
                        consultor = DualAIConsultation()
                        prompt = consultor._build_prompt(paciente['id'], cita['id'])
                        
                        # Consultar via n8n
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        resultado_n8n = loop.run_until_complete(
                            n8n_client.consultar_ias(prompt)
                        )
                        loop.close()
                        
                        if resultado_n8n:
                            # Verificar si la respuesta tiene el formato esperado del webhook del usuario
                            if 'deepseek_response' in resultado_n8n and 'copilot_response' in resultado_n8n:
                                # Convertir formato n8n a formato esperado por la UI
                                resultado = {
                                    'deepseek': {
                                        'diagnostico': resultado_n8n['deepseek_response'],
                                        'confianza': 0.0,  # Valor por defecto ya que n8n no devuelve confianza estructurada
                                        'error': False
                                    },
                                    'copilot': {
                                        'diagnostico': resultado_n8n['copilot_response'],
                                        'confianza': 0.0,  # Valor por defecto
                                        'error': False
                                    }
                                }
                                st.session_state['resultado_ia'] = resultado
                                st.success("✅ Consulta completada via n8n!")
                                st.rerun()
                            elif resultado_n8n.get('status') == 'success':
                                # Formato anterior (por si acaso)
                                resultado = {
                                    'deepseek': resultado_n8n['deepseek'],
                                    'copilot': resultado_n8n['copilot']
                                }
                                st.session_state['resultado_ia'] = resultado
                                st.success("✅ Consulta completada via n8n!")
                                st.rerun()
                            else:
                                st.warning("⚠️ Respuesta de n8n con formato inesperado, usando método directo...")
                                usar_n8n = False
                        else:
                            # Si n8n falla o devuelve None
                            st.warning("⚠️ n8n no devolvió respuesta, usando método directo...")
                            usar_n8n = False
                    
                    # Si n8n no está configurado o falló, usar método directo
                    if not usar_n8n:
                        consultor = DualAIConsultation()
                        
                        # Ejecutar consulta dual (asyncio)
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        resultado = loop.run_until_complete(
                            consultor.query_both_ais(paciente['id'], cita['id'])
                        )
                        loop.close()
                        
                        # Guardar en session state
                        st.session_state['resultado_ia'] = resultado
                        
                        st.success("✅ Consulta completada!")
                        st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Error al consultar IAs: {e}")
                    logger.error(f"Error en consulta dual: {e}")
                    
                    # Mostrar diagnóstico de prueba si las APIs no están configuradas
                    if "API" in str(e) or "key" in str(e).lower():
                        st.warning("⚠️ Las APIs no están configuradas. Mostrando diagnóstico de ejemplo...")
                        
                        resultado_ejemplo = {
                            'deepseek': {
                                'diagnostico': """## Evaluación de Eficacia Terapéutica Actual

El paciente muestra signos de actividad de enfermedad según los indicadores actuales. Se recomienda evaluación detallada del tratamiento actual.

## Riesgo de Progresión

Riesgo moderado basado en los indicadores presentados.

## Recomendaciones de Manejo

- Considerar ajuste de tratamiento actual
- Monitoreo cercano en próximas visitas
- Evaluación de adherencia al tratamiento

## Estudios Adicionales Sugeridos

- RM de seguimiento en 3 meses
- Análisis de biomarcadores

## Nivel de Confianza

**8/10** - Alta confianza basada en datos clínicos disponibles.""",
                                'confianza': 8.0,
                                'error': False
                            },
                            'copilot': {
                                'diagnostico': """## Evaluación de Eficacia Terapéutica Actual

Los indicadores sugieren necesidad de revisión del plan terapéutico actual.

## Riesgo de Progresión

Riesgo presente que requiere atención.

## Recomendaciones de Manejo

- Evaluar cambio de DMT
- Considerar terapia de escalada
- Seguimiento estrecho

## Estudios Adicionales Sugeridos

- RM cerebral y medular
- Evaluación neuropsicológica

## Nivel de Confianza

**7/10** - Confianza moderada-alta.""",
                                'confianza': 7.0,
                                'error': False
                            }
                        }
                        
                        st.session_state['resultado_ia'] = resultado_ejemplo
                        st.rerun()
    
    # Mostrar resultados si existen
    if 'resultado_ia' in st.session_state:
        resultado = st.session_state['resultado_ia']
        
        st.markdown("---")
        st.markdown("### 📊 Comparación de Diagnósticos")
        
        # Dos columnas para comparar
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔵 DeepSeek")
            
            deepseek = resultado['deepseek']
            
            if not deepseek.get('error'):
                st.markdown(deepseek['diagnostico'])
            else:
                st.error("Error al obtener diagnóstico de DeepSeek")
        
        with col2:
            st.markdown("#### 🟢 Microsoft Copilot")
            
            copilot = resultado['copilot']
            
            if not copilot.get('error'):
                st.markdown(copilot['diagnostico'])
            else:
                st.error("Error al obtener diagnóstico de Copilot")
        
        # Selección del médico
        st.markdown("---")
        st.markdown("### 👨‍⚕️ Selección del Médico")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Seleccionar DeepSeek", use_container_width=True):
                st.session_state['ia_seleccionada'] = 'deepseek'
        
        with col2:
            if st.button("✅ Seleccionar Copilot", use_container_width=True):
                st.session_state['ia_seleccionada'] = 'copilot'
        
        with col3:
            if st.button("✍️ Diagnóstico Propio", use_container_width=True):
                st.session_state['ia_seleccionada'] = 'medico'
        
        # Formulario de guardado
        if 'ia_seleccionada' in st.session_state:
            st.markdown("---")
            
            ia_sel = st.session_state['ia_seleccionada']
            
            if ia_sel == 'deepseek':
                st.success("✅ Has seleccionado el diagnóstico de **DeepSeek**")
            elif ia_sel == 'copilot':
                st.success("✅ Has seleccionado el diagnóstico de **Copilot**")
            else:
                st.info("✍️ Vas a escribir tu propio diagnóstico")
            
            with st.form("form_guardar_diagnostico"):
                diagnostico_medico = None
                
                if ia_sel == 'medico':
                    diagnostico_medico = st.text_area(
                        "Escribe tu diagnóstico:",
                        height=300,
                        placeholder="Ingresa tu evaluación clínica completa..."
                    )
                
                justificacion = st.text_area(
                    "Justificación de la selección (opcional):",
                    height=100,
                    placeholder="¿Por qué elegiste este diagnóstico?"
                )
                
                submitted = st.form_submit_button("💾 Guardar Diagnóstico", type="primary", use_container_width=True)
                
                if submitted:
                    try:
                        consultor = DualAIConsultation()
                        
                        consultor.save_results(
                            cita_id=cita['id'],
                            deepseek_response=resultado['deepseek'],
                            copilot_response=resultado['copilot'],
                            ia_seleccionada=ia_sel,
                            diagnostico_medico=diagnostico_medico,
                            justificacion=justificacion
                        )
                        
                        st.success("✅ Diagnóstico guardado exitosamente!")
                        st.balloons()
                        
                        # Limpiar session state
                        del st.session_state['resultado_ia']
                        del st.session_state['ia_seleccionada']
                        
                        logger.info(f"Diagnóstico IA guardado para cita {cita['id']}")
                    
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")
                        logger.error(f"Error al guardar diagnóstico: {e}")

# =====================================================
# TAB 2: HISTORIAL
# =====================================================
with tab2:
    st.markdown("### Historial de Diagnósticos del Paciente")
    
    try:
        # Obtener todas las citas con diagnósticos
        citas = db.listar_citas_paciente(paciente['id'])
        
        diagnosticos_encontrados = []
        
        for c in citas:
            try:
                diag = db.obtener_diagnostico_ia(c['id'])
                if diag:
                    diagnosticos_encontrados.append({
                        'cita': c,
                        'diagnostico': diag
                    })
            except:
                continue
        
        if not diagnosticos_encontrados:
            st.info("No hay diagnósticos de IA registrados para este paciente.")
        else:
            st.success(f"Se encontraron {len(diagnosticos_encontrados)} diagnósticos")
            
            # Mostrar cada diagnóstico
            for item in sorted(diagnosticos_encontrados, key=lambda x: x['cita']['numero_visita'], reverse=True):
                c = item['cita']
                diag = item['diagnostico']
                
                with st.expander(f"📋 Visita #{c['numero_visita']} - {c['fecha_cita'][:10]}"):
                    ia_sel = diag['ia_seleccionada']
                    
                    st.write(f"**IA Seleccionada:** {ia_sel.upper()}")
                    
                    if diag.get('justificacion_medico'):
                        st.write(f"**Justificación:** {diag['justificacion_medico']}")
                    
                    st.markdown("---")
                    
                    # Tabs para cada IA
                    tab_ds, tab_cp = st.tabs(["DeepSeek", "Copilot"])
                    
                    with tab_ds:
                        if diag.get('diagnostico_deepseek'):
                            st.markdown(diag['diagnostico_deepseek'])
                            st.caption(f"Confianza: {diag.get('confianza_deepseek', 'N/A')}/10")
                    
                    with tab_cp:
                        if diag.get('diagnostico_copilot'):
                            st.markdown(diag['diagnostico_copilot'])
                            st.caption(f"Confianza: {diag.get('confianza_copilot', 'N/A')}/10")
                    
                    if diag.get('diagnostico_medico_override'):
                        st.markdown("---")
                        st.markdown("**Diagnóstico del Médico:**")
                        st.markdown(diag['diagnostico_medico_override'])
    
    except Exception as e:
        st.error(f"Error al cargar historial: {e}")
