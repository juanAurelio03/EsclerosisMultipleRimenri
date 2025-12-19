# Script temporal para actualizar navegación en todas las páginas
import re

# Plantilla de navegación con barra fija
nav_template_start = '''# Barra de navegación inferior fija estilo móvil
st.markdown("""
<style>
    .bottom-nav-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 10px 5px;
        box-shadow: 0 -4px 12px rgba(0,0,0,0.15);
        z-index: 999;
    }
    
    .bottom-nav-container .stColumns {
        gap: 5px !important;
    }
    
    .bottom-nav-container button {
        height: 60px !important;
        font-size: 12px !important;
        border-radius: 12px !important;
        border: none !important;
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    
    .bottom-nav-container button:hover {
        background-color: rgba(255, 255, 255, 0.25) !important;
        transform: translateY(-2px) !important;
    }
    
    .bottom-nav-container button[kind="primary"] {
        background-color: white !important;
        color: #667eea !important;
        font-weight: bold !important;
    }
    
    /* Ajustar padding del contenido para la barra inferior */
    .main .block-container {
        padding-bottom: 100px !important;
    }
</style>

<div class="bottom-nav-container">
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("🏠\\nInicio", use_container_width=True{primary_home}, key="nav_home"):
        st.switch_page("app.py")

with col2:
    if st.button("📋\\nPacientes", use_container_width=True{primary_patients}, key="nav_patients"):
        st.switch_page("pages/1_📋_Gestión_de_Pacientes.py")

with col3:
    if st.button("📅\\nCitas", use_container_width=True{primary_citas}, key="nav_appointments"):
        st.switch_page("pages/2_📅_Sistema_de_Citas.py")

with col4:
    if st.button("🔬\\nIndicadores", use_container_width=True{primary_indicators}, key="nav_indicators"):
        st.switch_page("pages/3_🔬_Indicadores_Clínicos.py")

with col5:
    if st.button("🤖\\nIA", use_container_width=True{primary_ia}, key="nav_ai"):
        st.switch_page("pages/4_🤖_Consulta_IA.py")

with col6:
    if st.button("📊\\nDashboard", use_container_width=True{primary_dashboard}, key="nav_dashboard"):
        st.switch_page("pages/5_📊_Dashboard_Analítico.py")

st.markdown('</div>', unsafe_allow_html=True)'''

# Configuración para cada página
pages_config = {
    "2_📅_Sistema_de_Citas.py": "citas",
    "3_🔬_Indicadores_Clínicos.py": "indicators",
    "4_🤖_Consulta_IA.py": "ia",
    "5_📊_Dashboard_Analítico.py": "dashboard"
}

for page_file, primary_button in pages_config.items():
    file_path = f"d:/proyecto_rimenri/pages/{page_file}"
    
    # Leer archivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Preparar plantilla con botón primario correcto
    nav_code = nav_template_start.format(
        primary_home="" if primary_button != "home" else ", type=\"primary\"",
        primary_patients="" if primary_button != "patients" else ", type=\"primary\"",
        primary_citas="" if primary_button != "citas" else ", type=\"primary\"",
        primary_indicators="" if primary_button != "indicators" else ", type=\"primary\"",
        primary_ia="" if primary_button != "ia" else ", type=\"primary\"",
        primary_dashboard="" if primary_button != "dashboard" else ", type=\"primary\""
    )
    
    # Buscar y reemplazar el bloque de navegación
    pattern = r"# Barra de navegación inferior con botones de Streamlit.*?st\.markdown\('<div style=\"height: 20px;\"></div>', unsafe_allow_html=True\)"
    
    new_content = re.sub(pattern, nav_code, content, flags=re.DOTALL)
    
    # Escribir archivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Actualizado: {page_file}")

print("\n✅ Todas las páginas actualizadas con barra de navegación fija!")
