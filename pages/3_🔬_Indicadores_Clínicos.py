"""
Página de Indicadores Clínicos
"""
import streamlit as st
from datetime import datetime
from decimal import Decimal
import sys
from pathlib import Path
import pandas as pd

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.database import db
from src.calculators import IndicatorCalculator
from config import TipoIndicador, EstadoIndicador, StreamlitConfig
from loguru import logger

st.set_page_config(page_title="Indicadores Clínicos", page_icon="🔬", layout="wide", initial_sidebar_state="collapsed")

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
    if st.button("🔬\nIndicadores", use_container_width=True, type="primary", key="nav_indicators"):
        st.switch_page("pages/3_🔬_Indicadores_Clínicos.py")

with col5:
    if st.button("🤖\nIA", use_container_width=True, key="nav_ai"):
        st.switch_page("pages/4_🤖_Consulta_IA.py")

with col6:
    if st.button("📊\nDashboard", use_container_width=True, key="nav_dashboard"):
        st.switch_page("pages/5_📊_Dashboard_Analítico.py")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">🔬 Registro de Indicadores Clínicos</div>', unsafe_allow_html=True)

# Verificar paciente y cita
if not st.session_state.get('paciente_seleccionado'):
    st.warning("⚠️ No hay paciente seleccionado.")
    st.stop()

if not st.session_state.get('cita_actual'):
    st.warning("⚠️ No hay cita activa. Selecciona una cita en el Sistema de Citas.")
    st.stop()

paciente = st.session_state.paciente_seleccionado
cita = st.session_state.cita_actual

st.info(f"**Paciente:** {paciente['nombre_completo']} | **Cita:** Visita #{cita['numero_visita']} - {cita['fecha_cita'][:10]}")

# Tabs para organizar los indicadores
tab1, tab2, tab3 = st.tabs(["📝 Registrar Indicadores", "📊 Resultados", "📈 Historial"])

# =====================================================
# TAB 1: REGISTRAR INDICADORES
# =====================================================
with tab1:
    st.markdown("### Ingresar Variables Clínicas")
    
    # Subtabs para cada tipo de dato
    subtab1, subtab2, subtab3 = st.tabs(["🔄 Recaídas", "🧠 Resonancia Magnética", "📏 EDSS"])
    
    # Variables para almacenar datos
    if 'indicadores_data' not in st.session_state:
        st.session_state.indicadores_data = {}
    
    with subtab1:
        st.markdown("#### Recaídas desde Última Visita")
        
        # Obtener fecha de última visita
        citas_anteriores = db.listar_citas_paciente(paciente['id'])
        citas_anteriores = [c for c in citas_anteriores if c['numero_visita'] < cita['numero_visita']]
        
        if citas_anteriores:
            ultima_visita = max(citas_anteriores, key=lambda x: x['numero_visita'])
            st.info(f"📅 Última visita: #{ultima_visita['numero_visita']} - {ultima_visita['fecha_cita'][:10]}")
        else:
            st.info("Esta es la primera visita del paciente")
        
        recaidas = st.number_input(
            "Número de recaídas desde última visita:",
            min_value=0,
            max_value=50,
            value=0,
            step=1,
            help="Número total de recaídas clínicas documentadas"
        )
        
        st.session_state.indicadores_data['recaidas'] = recaidas
    
    with subtab2:
        st.markdown("#### Lesiones en Resonancia Magnética")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Lesiones T1 con Gadolinio (Gd+)**")
            lesiones_t1_gd = st.number_input(
                "Conteo de lesiones T1 Gd+:",
                min_value=0,
                max_value=100,
                value=0,
                step=1,
                help="Número de lesiones que captan gadolinio (actividad inflamatoria)"
            )
            st.session_state.indicadores_data['lesiones_t1_gd'] = lesiones_t1_gd
        
        with col2:
            st.markdown("**Lesiones T2**")
            lesiones_t2_actuales = st.number_input(
                "Conteo actual de lesiones T2:",
                min_value=0,
                max_value=200,
                value=0,
                step=1,
                help="Número total de lesiones T2 en el estudio actual"
            )
            st.session_state.indicadores_data['lesiones_t2_actuales'] = lesiones_t2_actuales
        
        # Obtener T2 previas
        lesiones_t2_previas = 0
        if citas_anteriores:
            for cita_ant in sorted(citas_anteriores, key=lambda x: x['numero_visita'], reverse=True):
                indicadores_ant = db.obtener_indicadores_cita(cita_ant['id'])
                for ind in indicadores_ant:
                    if ind['indicador_tipo'] == 'T2_nuevas':
                        vars_entrada = ind.get('variables_entrada', {})
                        lesiones_t2_previas = vars_entrada.get('lesiones_t2_actuales', 0)
                        break
                if lesiones_t2_previas > 0:
                    break
        
        st.info(f"📊 Lesiones T2 previas: {lesiones_t2_previas}")
        st.session_state.indicadores_data['lesiones_t2_previas'] = lesiones_t2_previas
    
    with subtab3:
        st.markdown("#### Escala EDSS")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("EDSS Basal", paciente['edss_basal'])
        
        with col2:
            edss_actual = st.select_slider(
                "EDSS Actual:",
                options=[i * 0.5 for i in range(21)],
                value=float(paciente['edss_basal']),
                help="Expanded Disability Status Scale actual"
            )
            st.session_state.indicadores_data['edss_actual'] = edss_actual
    
    # Verificar si ya existen indicadores
    indicadores_existentes = None
    try:
        indicadores_existentes = db.obtener_indicadores_cita(cita['id'])
    except:
        pass
    
    # Advertencia si ya existen indicadores
    if indicadores_existentes:
        st.warning(f"⚠️ Ya existen {len(indicadores_existentes)} indicadores calculados para esta cita.")
        recalcular = st.checkbox("Recalcular indicadores (sobrescribirá los existentes)")
        if not recalcular:
            st.info("💡 Marca la casilla de arriba si deseas recalcular los indicadores.")
            st.stop()
    
    # Botón para calcular indicadores
    st.markdown("---")
    boton_texto = "🔄 Recalcular Indicadores" if indicadores_existentes else "🔬 Calcular Indicadores"
    
    if st.button(boton_texto, type="primary", use_container_width=True):
        try:
            with st.spinner("Calculando indicadores..."):
                data = st.session_state.indicadores_data
                
                # Calcular cada indicador
                indicadores_calculados = []
                
                # 1. ARR
                # Convertir fecha_diagnostico a datetime con timezone
                from datetime import timezone
                fecha_inicio = datetime.fromisoformat(paciente['fecha_diagnostico'])
                # Agregar timezone UTC si no tiene
                if fecha_inicio.tzinfo is None:
                    fecha_inicio = fecha_inicio.replace(tzinfo=timezone.utc)
                
                fecha_fin = datetime.fromisoformat(cita['fecha_cita'].replace('Z', '+00:00'))
                
                arr_valor, arr_estado, arr_just = IndicatorCalculator.calculate_arr(
                    data['recaidas'],
                    fecha_inicio,
                    fecha_fin
                )
                
                indicadores_calculados.append({
                    'cita_id': cita['id'],
                    'indicador_tipo': 'ARR',
                    'valor_calculado': float(arr_valor),
                    'estado': arr_estado.value,
                    'justificacion_texto': arr_just,
                    'variables_entrada': {'recaidas': data['recaidas']}
                })
                
                # 2. T1 Gd+
                t1_estado, t1_just = IndicatorCalculator.classify_t1_gd(data['lesiones_t1_gd'])
                
                indicadores_calculados.append({
                    'cita_id': cita['id'],
                    'indicador_tipo': 'T1_Gd',
                    'valor_calculado': float(data['lesiones_t1_gd']),
                    'estado': t1_estado.value,
                    'justificacion_texto': t1_just,
                    'variables_entrada': {'lesiones_t1_gd': data['lesiones_t1_gd']}
                })
                
                # 3. T2 nuevas
                t2_diff, t2_estado, t2_just = IndicatorCalculator.calculate_t2_difference(
                    data['lesiones_t2_actuales'],
                    data['lesiones_t2_previas']
                )
                
                indicadores_calculados.append({
                    'cita_id': cita['id'],
                    'indicador_tipo': 'T2_nuevas',
                    'valor_calculado': float(t2_diff),
                    'estado': t2_estado.value,
                    'justificacion_texto': t2_just,
                    'variables_entrada': {
                        'lesiones_t2_actuales': data['lesiones_t2_actuales'],
                        'lesiones_t2_previas': data['lesiones_t2_previas']
                    }
                })
                
                # 4. CDP-12
                cdp_delta, cdp_prog, cdp_estado, cdp_just = IndicatorCalculator.evaluate_cdp12(
                    Decimal(str(paciente['edss_basal'])),
                    Decimal(str(data['edss_actual']))
                )
                
                indicadores_calculados.append({
                    'cita_id': cita['id'],
                    'indicador_tipo': 'CDP12',
                    'valor_calculado': float(cdp_delta),
                    'estado': cdp_estado.value,
                    'justificacion_texto': cdp_just,
                    'variables_entrada': {
                        'edss_basal': float(paciente['edss_basal']),
                        'edss_actual': data['edss_actual'],
                        'progresion_confirmada': cdp_prog
                    }
                })
                
                # 5. NEDA-3
                sin_recaidas = data['recaidas'] == 0
                sin_lesiones_rm = (data['lesiones_t1_gd'] == 0 and t2_diff <= 0)
                sin_progresion = not cdp_prog
                
                neda_cumple, neda_estado, neda_just, neda_detalles = IndicatorCalculator.evaluate_neda3(
                    sin_recaidas,
                    sin_lesiones_rm,
                    sin_progresion
                )
                
                indicadores_calculados.append({
                    'cita_id': cita['id'],
                    'indicador_tipo': 'NEDA3',
                    'valor_calculado': 1.0 if neda_cumple else 0.0,
                    'estado': neda_estado.value,
                    'justificacion_texto': neda_just,
                    'variables_entrada': neda_detalles
                })
                
                # Guardar en base de datos
                for ind in indicadores_calculados:
                    db.guardar_indicador(ind)
                
                # Actualizar estado de la cita
                db.actualizar_cita(cita['id'], {'estado': 'completada'})
                
                # Enviar alertas críticas via n8n (si está configurado)
                try:
                    from src.n8n import n8n_client
                    import asyncio
                    
                    # Verificar si hay indicadores críticos
                    indicadores_criticos = [ind for ind in indicadores_calculados if ind['estado'] == 'critico']
                    
                    if indicadores_criticos and n8n_client.is_configured():
                        for ind_critico in indicadores_criticos:
                            # Enviar alerta de forma asíncrona
                            alerta_enviada = asyncio.run(
                                n8n_client.enviar_alerta_critica(ind_critico, paciente, cita)
                            )
                            if alerta_enviada:
                                st.info(f"🔔 Alerta enviada para indicador crítico: {ind_critico['indicador_tipo']}")
                except Exception as e:
                    logger.warning(f"No se pudo enviar alerta via n8n: {e}")
                
                st.session_state['indicadores_calculados'] = indicadores_calculados
                st.success("✅ Indicadores calculados y guardados exitosamente!")
                st.balloons()
                
                logger.info(f"Indicadores calculados para cita {cita['id']}")
        
        except Exception as e:
            st.error(f"Error al calcular indicadores: {e}")
            logger.error(f"Error en cálculo de indicadores: {e}")

# =====================================================
# TAB 2: RESULTADOS
# =====================================================
with tab2:
    st.markdown("### Resultados de Indicadores")
    
    try:
        indicadores = db.obtener_indicadores_cita(cita['id'])
        
        if not indicadores:
            st.info("No hay indicadores calculados para esta cita. Ve a la pestaña 'Registrar Indicadores'.")
        else:
            # Mostrar cada indicador con su color
            for ind in indicadores:
                estado = ind['estado']
                tipo = ind['indicador_tipo']
                valor = ind.get('valor_calculado', 'N/A')
                just = ind['justificacion_texto']
                
                # Determinar clase CSS
                css_class = f"indicator-{estado}"
                
                # Emoji según estado
                emoji = {'normal': '✅', 'alerta': '⚠️', 'critico': '🔴'}[estado]
                
                st.markdown(f"""
                <div class="{css_class}">
                    <h4>{emoji} {tipo}: {valor}</h4>
                    <p>{just}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Resumen en tabla
            st.markdown("---")
            st.markdown("#### 📊 Resumen de Indicadores")
            
            df_data = []
            for ind in indicadores:
                df_data.append({
                    'Indicador': ind['indicador_tipo'],
                    'Valor': ind.get('valor_calculado', 'N/A'),
                    'Estado': ind['estado'].upper(),
                    'Clasificación': {'normal': '🟢', 'alerta': '🟡', 'critico': '🔴'}[ind['estado']]
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error al cargar resultados: {e}")

# =====================================================
# TAB 3: HISTORIAL
# =====================================================
with tab3:
    st.markdown("### Historial de Indicadores del Paciente")
    
    try:
        # Selector de indicador
        tipo_indicador = st.selectbox(
            "Selecciona indicador:",
            options=['ARR', 'T1_Gd', 'T2_nuevas', 'CDP12', 'NEDA3']
        )
        
        historial = db.obtener_historial_indicadores(paciente['id'], tipo_indicador)
        
        if not historial:
            st.info(f"No hay historial de {tipo_indicador} para este paciente.")
        else:
            # Crear DataFrame para gráfico
            data = []
            for h in historial:
                cita_data = h.get('citas', {})
                data.append({
                    'Fecha': cita_data.get('fecha_cita', '')[:10],
                    'Valor': h.get('valor_calculado', 0),
                    'Estado': h.get('estado', 'normal')
                })
            
            df = pd.DataFrame(data)
            df['Fecha'] = pd.to_datetime(df['Fecha'])
            df = df.sort_values('Fecha')
            
            # Gráfico de línea
            import plotly.graph_objects as go
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['Fecha'],
                y=df['Valor'],
                mode='lines+markers',
                name=tipo_indicador,
                line=dict(width=3),
                marker=dict(size=10)
            ))
            
            fig.update_layout(
                title=f"Evolución de {tipo_indicador}",
                xaxis_title="Fecha",
                yaxis_title="Valor",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabla de datos
            st.dataframe(df, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error al cargar historial: {e}")
