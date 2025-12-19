# Script para actualizar navegación en todas las páginas
import re

# CSS mejorado para navegación
nav_css = '''# Barra de navegación superior fija y mejorada
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
""", unsafe_allow_html=True)'''

# Archivos a actualizar con su botón primario
pages = {
    "d:/proyecto_rimenri/pages/1_📋_Gestión_de_Pacientes.py": "nav_patients",
    "d:/proyecto_rimenri/pages/2_📅_Sistema_de_Citas.py": "nav_appointments",
    "d:/proyecto_rimenri/pages/3_🔬_Indicadores_Clínicos.py": "nav_indicators",
    "d:/proyecto_rimenri/pages/4_🤖_Consulta_IA.py": "nav_ai",
    "d:/proyecto_rimenri/pages/5_📊_Dashboard_Analítico.py": "nav_dashboard"
}

for file_path, primary_key in pages.items():
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar el bloque de navegación
        pattern = r'# Barra de navegación.*?<div class="bottom-nav-container">.*?\"\"\", unsafe_allow_html=True\)'
        
        # Reemplazar con el nuevo CSS
        new_content = re.sub(pattern, nav_css, content, flags=re.DOTALL)
        
        # Actualizar el botón primario correcto
        # Primero quitar todos los type="primary"
        new_content = re.sub(r', type="primary"', '', new_content)
        
        # Agregar type="primary" al botón correcto
        new_content = re.sub(
            f'(if st.button\\([^,]+, use_container_width=True)(, key="{primary_key}")',
            r'\1, type="primary"\2',
            new_content
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Actualizado: {file_path.split('/')[-1]}")
    except Exception as e:
        print(f"❌ Error en {file_path.split('/')[-1]}: {e}")

print("\n✅ Todas las páginas actualizadas con navegación mejorada!")
