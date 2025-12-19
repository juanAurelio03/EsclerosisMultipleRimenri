"""
Página de Dashboard Analítico
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path
from datetime import datetime

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.database import db
from loguru import logger

st.set_page_config(page_title="Dashboard Analítico", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

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
    if st.button("🤖\nIA", use_container_width=True, key="nav_ai"):
        st.switch_page("pages/4_🤖_Consulta_IA.py")

with col6:
    if st.button("📊\nDashboard", use_container_width=True, type="primary", key="nav_dashboard"):
        st.switch_page("pages/5_📊_Dashboard_Analítico.py")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">📊 Dashboard Analítico</div>', unsafe_allow_html=True)

# Tabs - AI Metrics first, always visible
tab1, tab2 = st.tabs(["🤖 Métricas de IAs", "👤 Análisis del Paciente"])

# =====================================================
# TAB 1: MÉTRICAS DE IAs (SIEMPRE VISIBLE)
# =====================================================
with tab1:
    st.markdown("### Análisis de Precisión de las IAs")
    
    st.info("""
    📊 **Métricas de Accuracy:**
    - **Accuracy** = (Veces seleccionada / Total consultas) × 100
    - Una IA es "seleccionada" cuando el médico elige su diagnóstico
    - Si el médico escribe su propio diagnóstico, se cuenta como "override"
    - **IA con más aciertos** = La que tiene mayor porcentaje de selecciones
    """)
    
    try:
        # Calcular métricas
        metricas = db.calcular_metricas_ia()
        
        if not metricas or metricas.get('total_consultas', 0) == 0:
            st.warning("⚠️ No hay suficientes datos de consultas a IAs para generar métricas.")
            st.info("💡 Las métricas se generarán automáticamente cuando uses la función de **Consulta IA** con pacientes.")
        else:
            # Calcular cuál IA tiene más aciertos
            acc_ds = float(metricas.get('accuracy_deepseek', 0))
            acc_cp = float(metricas.get('accuracy_copilot', 0))
            
            if acc_ds > acc_cp:
                ia_ganadora = "DeepSeek"
                acc_ganadora = acc_ds
                emoji_ganadora = "🥇"
            elif acc_cp > acc_ds:
                ia_ganadora = "Copilot"
                acc_ganadora = acc_cp
                emoji_ganadora = "🥇"
            else:
                ia_ganadora = "Empate"
                acc_ganadora = acc_ds
                emoji_ganadora = "🤝"
            
            # Banner destacado con la IA ganadora
            if ia_ganadora != "Empate":
                # Color según la IA ganadora
                color = "#1f77b4" if ia_ganadora == "DeepSeek" else "#2ca02c"
                st.markdown(f"""
                <div style="background-color: {color}; color: white; padding: 25px; 
                            border-radius: 10px; text-align: center; margin-bottom: 25px;
                            box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                    <h3 style="margin: 0 0 10px 0; font-size: 1.2em; opacity: 0.9;">🏆 IA CON MÁS ACIERTOS</h3>
                    <h1 style="margin: 0; font-size: 3em; font-weight: bold;">{ia_ganadora}</h1>
                    <p style="margin: 10px 0 0 0; font-size: 1.8em; font-weight: 500;">{acc_ganadora:.1f}% de Accuracy</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: #6c757d; color: white; padding: 25px; 
                            border-radius: 10px; text-align: center; margin-bottom: 25px;
                            box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                    <h3 style="margin: 0 0 10px 0; font-size: 1.2em; opacity: 0.9;">🤝 RESULTADO</h3>
                    <h1 style="margin: 0; font-size: 3em; font-weight: bold;">Empate Técnico</h1>
                    <p style="margin: 10px 0 0 0; font-size: 1.8em; font-weight: 500;">Ambas IAs: {acc_ganadora:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Métricas principales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Consultas", metricas.get('total_consultas', 0))
            
            with col2:
                delta_ds = "🥇" if acc_ds > acc_cp else ("🥈" if acc_ds < acc_cp else "🤝")
                st.metric("Accuracy DeepSeek", f"{acc_ds:.1f}%", delta=delta_ds)
            
            with col3:
                delta_cp = "🥇" if acc_cp > acc_ds else ("🥈" if acc_cp < acc_ds else "🤝")
                st.metric("Accuracy Copilot", f"{acc_cp:.1f}%", delta=delta_cp)
            
            with col4:
                acc_medico = (metricas.get('selecciones_medico_override', 0) / metricas.get('total_consultas', 1) * 100)
                st.metric("Override Médico", f"{acc_medico:.1f}%")
            
            st.markdown("---")
            
            # Gráfico de barras comparativo
            st.markdown("#### 📊 Comparación de Accuracy")
            
            df_metricas = pd.DataFrame({
                'IA': ['DeepSeek', 'Copilot'],
                'Accuracy (%)': [acc_ds, acc_cp],
                'Selecciones': [
                    metricas.get('selecciones_deepseek', 0),
                    metricas.get('selecciones_copilot', 0)
                ]
            })
            
            fig = px.bar(
                df_metricas,
                x='IA',
                y='Accuracy (%)',
                text='Accuracy (%)',
                color='IA',
                color_discrete_map={'DeepSeek': '#1f77b4', 'Copilot': '#2ca02c'}
            )
            
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(height=400, showlegend=False)
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # Tabla detallada
            st.markdown("#### 📋 Tabla de Métricas Detalladas")
            
            df_detalle = pd.DataFrame({
                'IA': ['DeepSeek', 'Copilot', 'Médico (Override)'],
                'Selecciones': [
                    metricas.get('selecciones_deepseek', 0),
                    metricas.get('selecciones_copilot', 0),
                    metricas.get('selecciones_medico_override', 0)
                ],
                'Total Consultas': [
                    metricas.get('total_consultas', 0),
                    metricas.get('total_consultas', 0),
                    metricas.get('total_consultas', 0)
                ],
                'Accuracy (%)': [
                    acc_ds,
                    acc_cp,
                    acc_medico
                ]
            })
            
            st.dataframe(df_detalle, use_container_width=True)
            
            # Gráfico de distribución
            st.markdown("---")
            st.markdown("#### 🥧 Distribución de Selecciones")
            
            fig_pie = px.pie(
                df_detalle,
                values='Selecciones',
                names='IA',
                title='Distribución de Diagnósticos Seleccionados'
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Evolución temporal (si hay historial)
            st.markdown("---")
            st.markdown("#### 📈 Evolución Temporal de Accuracy")
            
            try:
                historial_metricas = db.obtener_historial_metricas_ia(limite=30)
                
                if historial_metricas:
                    df_hist = pd.DataFrame(historial_metricas)
                    df_hist['fecha_calculo'] = pd.to_datetime(df_hist['fecha_calculo'])
                    df_hist = df_hist.sort_values('fecha_calculo')
                    
                    fig_evol = go.Figure()
                    
                    fig_evol.add_trace(go.Scatter(
                        x=df_hist['fecha_calculo'],
                        y=df_hist['accuracy_deepseek'],
                        mode='lines+markers',
                        name='DeepSeek',
                        line=dict(color='#1f77b4', width=3)
                    ))
                    
                    fig_evol.add_trace(go.Scatter(
                        x=df_hist['fecha_calculo'],
                        y=df_hist['accuracy_copilot'],
                        mode='lines+markers',
                        name='Copilot',
                        line=dict(color='#2ca02c', width=3)
                    ))
                    
                    fig_evol.update_layout(
                        title='Evolución de Accuracy a lo Largo del Tiempo',
                        xaxis_title='Fecha',
                        yaxis_title='Accuracy (%)',
                        hovermode='x unified',
                        height=400
                    )
                    
                    st.plotly_chart(fig_evol, use_container_width=True)
                else:
                    st.info("No hay historial de métricas disponible")
            
            except Exception as e:
                st.warning(f"No se pudo cargar evolución temporal: {e}")
    
    except Exception as e:
        st.error(f"Error al calcular métricas de IA: {e}")
        logger.error(f"Error en métricas de IA: {e}")

# =====================================================
# TAB 2: ANÁLISIS DEL PACIENTE
# =====================================================
with tab2:
    # Verificar paciente seleccionado
    if not st.session_state.get('paciente_seleccionado'):
        st.warning("⚠️ No hay paciente seleccionado. Selecciona un paciente en Gestión de Pacientes.")
        st.stop()
    
    paciente = st.session_state.paciente_seleccionado
    
    st.markdown(f"### Análisis de Evolución: {paciente['nombre_completo']}")
    
    try:
        # Obtener historial de citas
        citas = db.listar_citas_paciente(paciente['id'])
        citas_completadas = [c for c in citas if c.get('estado') == 'completada']
        
        if not citas_completadas:
            st.info("No hay citas completadas para este paciente. Los gráficos se mostrarán cuando haya datos disponibles.")
        else:
            # Métricas generales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Visitas", len(citas_completadas))
            
            with col2:
                from datetime import timezone
                primera_cita = min(citas_completadas, key=lambda x: x['fecha_cita'])
                fecha_primera = datetime.fromisoformat(primera_cita['fecha_cita'].replace('Z', '+00:00'))
                # Hacer datetime.now() timezone-aware
                ahora = datetime.now(timezone.utc)
                meses_seguimiento = (ahora - fecha_primera).days / 30
                st.metric("Meses de Seguimiento", f"{meses_seguimiento:.1f}")
            
            with col3:
                st.metric("Tipo de EM", paciente['tipo_em'])
            
            with col4:
                st.metric("EDSS Basal", paciente['edss_basal'])
            
            st.markdown("---")
            
            # Gráfico 1: Evolución de Indicadores
            st.markdown("#### 📈 Evolución de Indicadores Clínicos")
            
            # Selector de indicadores a mostrar
            indicadores_disponibles = ['ARR', 'T1_Gd', 'T2_nuevas', 'CDP12']
            indicadores_seleccionados = st.multiselect(
                "Selecciona indicadores para visualizar:",
                options=indicadores_disponibles,
                default=['ARR', 'CDP12']
            )
            
            if indicadores_seleccionados:
                # Crear gráfico
                fig = go.Figure()
                
                for tipo_ind in indicadores_seleccionados:
                    historial = db.obtener_historial_indicadores(paciente['id'], tipo_ind)
                    
                    if historial:
                        fechas = []
                        valores = []
                        estados = []
                        
                        for h in historial:
                            cita_data = h.get('citas', {})
                            fechas.append(cita_data.get('fecha_cita', '')[:10])
                            valores.append(float(h.get('valor_calculado', 0)))
                            estados.append(h.get('estado', 'normal'))
                        
                        fig.add_trace(go.Scatter(
                            x=fechas,
                            y=valores,
                            mode='lines+markers',
                            name=tipo_ind,
                            line=dict(width=3),
                            marker=dict(size=10)
                        ))
                
                fig.update_layout(
                    title="Evolución Temporal de Indicadores",
                    xaxis_title="Fecha de Visita",
                    yaxis_title="Valor del Indicador",
                    hovermode='x unified',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # Gráfico 2: Heatmap NEDA-3
            st.markdown("#### 🔥 Heatmap NEDA-3")
            
            historial_neda = db.obtener_historial_indicadores(paciente['id'], 'NEDA3')
            
            if historial_neda:
                data_neda = []
                for h in historial_neda:
                    cita_data = h.get('citas', {})
                    cumple = h.get('valor_calculado', 0) == 1.0
                    data_neda.append({
                        'Fecha': cita_data.get('fecha_cita', '')[:10],
                        'NEDA-3': 'Cumple' if cumple else 'No Cumple',
                        'Valor': 1 if cumple else 0
                    })
                
                df_neda = pd.DataFrame(data_neda)
                
                fig = px.bar(
                    df_neda,
                    x='Fecha',
                    y='Valor',
                    color='NEDA-3',
                    color_discrete_map={'Cumple': '#28a745', 'No Cumple': '#dc3545'},
                    title='Cumplimiento NEDA-3 por Visita'
                )
                
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Estadísticas NEDA-3
                cumple_count = len([d for d in data_neda if d['NEDA-3'] == 'Cumple'])
                total_count = len(data_neda)
                porcentaje = (cumple_count / total_count * 100) if total_count > 0 else 0
                
                st.metric("Porcentaje de Cumplimiento NEDA-3", f"{porcentaje:.1f}%")
            else:
                st.info("No hay datos de NEDA-3 disponibles")
            
            st.markdown("---")
            
            # Tabla de resumen de última visita
            st.markdown("#### 📋 Resumen de Última Visita")
            
            ultima_cita = max(citas_completadas, key=lambda x: x['fecha_cita'])
            indicadores_ultima = db.obtener_indicadores_cita(ultima_cita['id'])
            
            if indicadores_ultima:
                df_data = []
                for ind in indicadores_ultima:
                    emoji = {'normal': '🟢', 'alerta': '🟡', 'critico': '🔴'}[ind['estado']]
                    df_data.append({
                        'Indicador': ind['indicador_tipo'],
                        'Valor': ind.get('valor_calculado', 'N/A'),
                        'Estado': f"{emoji} {ind['estado'].upper()}",
                        'Justificación': ind['justificacion_texto'][:100] + '...'
                    })
                
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error al cargar análisis del paciente: {e}")
        logger.error(f"Error en dashboard del paciente: {e}")

