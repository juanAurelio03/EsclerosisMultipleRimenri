# Guía de Uso - Workflows n8n Corregidos

## ✅ Cambios Realizados

Los workflows han sido corregidos y simplificados para funcionar correctamente en n8n:

### Correcciones Principales:
1. ✅ Uso de nodos `Code` en lugar de `Function` (compatible con n8n moderno)
2. ✅ Estructura de IDs única para cada nodo
3. ✅ Expresiones correctas con sintaxis `={{  }}`
4. ✅ Configuración simplificada de HTTP requests
5. ✅ Eliminación de dependencias complejas

## 📋 Workflows Disponibles

### 1. AI Dual Consultation (`ai_orchestration.json`)

**Funcionalidad**: Consulta paralela a DeepSeek y Copilot

**Cómo funciona**:
1. Recibe webhook con `prompt` en el body
2. Envía consulta a DeepSeek API
3. Envía consulta a Copilot API (en paralelo)
4. Parsea respuestas y extrae confianza
5. Combina resultados en JSON

**Payload de ejemplo**:
```json
{
  "prompt": "Analiza este caso de EM: paciente de 35 años con ARR de 0.25..."
}
```

**Respuesta**:
```json
{
  "deepseek": {
    "diagnostico": "...",
    "confianza": 8.0,
    "ia": "deepseek"
  },
  "copilot": {
    "diagnostico": "...",
    "confianza": 7.5,
    "ia": "copilot"
  },
  "timestamp": "2025-11-28T16:00:00.000Z",
  "status": "success"
}
```

### 2. Appointment Reminders (`appointment_reminders.json`)

**Funcionalidad**: Recordatorios automáticos de citas

**Programación**: Diario a las 9:00 AM

**Proceso**:
1. Consulta Supabase por citas en próximas 48h
2. Divide en items individuales
3. Formatea mensaje personalizado
4. Envía email a cada paciente

### 3. Critical Alerts (`critical_alerts.json`)

**Funcionalidad**: Alertas inmediatas de indicadores críticos

**Proceso**:
1. Recibe webhook con datos del indicador
2. Valida que sea crítico
3. Formatea mensaje de alerta
4. Envía email de alta prioridad

**Payload de ejemplo**:
```json
{
  "indicador": {
    "tipo": "ARR",
    "valor": 0.25,
    "estado": "critico",
    "justificacion": "ARR supera umbral..."
  },
  "paciente": {
    "nombre_completo": "María González"
  },
  "cita": {
    "numero_visita": 5
  }
}
```

## 🔧 Configuración en n8n

### Paso 1: Importar Workflows

1. Abre n8n en tu navegador
2. Click en **Workflows** → **Import from File**
3. Selecciona cada archivo JSON
4. Click **Import**

### Paso 2: Configurar Variables de Entorno

En n8n, ve a **Settings** → **Environments** y agrega:

```env
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx
COPILOT_API_KEY=sk-xxxxxxxxxxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Paso 3: Configurar Credenciales SMTP

Para los workflows de email:

1. Ve a **Credentials** → **Create New**
2. Selecciona **SMTP**
3. Configura:
   - **Host**: smtp.gmail.com
   - **Port**: 587
   - **User**: tu-email@gmail.com
   - **Password**: tu-app-password
   - **Secure**: TLS

### Paso 4: Activar Workflows

1. Abre cada workflow
2. Click en el toggle **Active** (arriba a la derecha)
3. Verifica que esté en verde

## 🧪 Testing

### Test AI Orchestration:

```bash
# Obtener URL del webhook
# En n8n, abre el workflow y copia la URL del nodo Webhook

curl -X POST https://tu-n8n.app.n8n.cloud/webhook/ai-consultation \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Paciente de 35 años con EM tipo EMRR. ARR actual: 0.25. EDSS: 3.5. ¿Qué recomiendas?"
  }'
```

### Test Critical Alert:

```bash
curl -X POST https://tu-n8n.app.n8n.cloud/webhook/critical-alert \
  -H "Content-Type: application/json" \
  -d '{
    "indicador": {
      "tipo": "ARR",
      "valor": 0.25,
      "estado": "critico",
      "justificacion": "ARR de 0.25 supera umbral de 0.20"
    },
    "paciente": {
      "nombre_completo": "Test Patient"
    },
    "cita": {
      "numero_visita": 1
    }
  }'
```

## 🔗 Integración con Streamlit

### En tu código Python:

```python
import httpx
import asyncio

# URL del webhook (cópiala desde n8n)
N8N_AI_WEBHOOK = "https://tu-n8n.app.n8n.cloud/webhook/ai-consultation"

async def consultar_ias_n8n(prompt: str):
    """Consulta a las IAs via n8n"""
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            N8N_AI_WEBHOOK,
            json={"prompt": prompt}
        )
        return response.json()

# Uso en Streamlit
if st.button("Consultar IAs"):
    with st.spinner("Consultando..."):
        resultado = asyncio.run(consultar_ias_n8n(prompt_medico))
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### DeepSeek")
            st.write(resultado['deepseek']['diagnostico'])
        with col2:
            st.markdown("### Copilot")
            st.write(resultado['copilot']['diagnostico'])
```

## ⚠️ Troubleshooting

### Error: "Workflow could not be activated"
- Verifica que las variables de entorno estén configuradas
- Revisa que las credenciales SMTP estén creadas

### Error: "Authentication failed"
- Verifica las API keys de DeepSeek y Copilot
- Asegúrate de usar el formato correcto: `Bearer sk-xxxxx`

### Error: "Timeout"
- Las APIs pueden tardar. Aumenta timeout en nodos HTTP
- Verifica conectividad a internet

### Emails no se envían
- Verifica credenciales SMTP
- Si usas Gmail, activa "App Passwords"
- Revisa spam/correo no deseado

## 📊 Monitoreo

1. **Ver Ejecuciones**: n8n → Executions
2. **Ver Logs**: Click en cada ejecución para detalles
3. **Errores**: Se muestran en rojo con mensaje de error

## 🎯 Próximos Pasos

1. Importa los 3 workflows
2. Configura variables de entorno
3. Configura SMTP
4. Activa workflows
5. Prueba con curl
6. Integra con Streamlit

¡Los workflows están listos para usar! 🚀
