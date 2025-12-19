# 🔗 Integración n8n con Streamlit

## ✅ Integración Completada

He integrado los workflows de n8n con tu aplicación Streamlit. Ahora tienes dos formas de usar las IAs:

### 1. **Método Directo** (por defecto)
- Llama directamente a las APIs de DeepSeek y Copilot
- No requiere n8n
- Funciona con solo las API keys en `.env`

### 2. **Método n8n** (opcional, recomendado)
- Usa n8n como orquestador
- Más eficiente y escalable
- Permite monitoreo centralizado
- Requiere n8n corriendo

---

## 📁 Archivos Creados/Modificados

### Nuevos Archivos:
1. **`src/n8n/n8n_client.py`** - Cliente para webhooks de n8n
2. **`src/n8n/__init__.py`** - Módulo n8n

### Archivos Modificados:
1. **`pages/3_🔬_Indicadores_Clínicos.py`** - Envía alertas críticas automáticamente
2. **`pages/4_🤖_Consulta_IA.py`** - Opción de usar n8n para consultas
3. **`.env.example`** - Variables de n8n agregadas

---

## 🚀 Cómo Funciona

### Alertas Críticas Automáticas

Cuando calculas indicadores y alguno es **crítico** (🔴):

```python
# En Indicadores Clínicos
if indicador['estado'] == 'critico':
    # Se envía automáticamente via n8n
    n8n_client.enviar_alerta_critica(indicador, paciente, cita)
    # ↓
    # n8n recibe el webhook
    # ↓
    # Formatea el mensaje
    # ↓
    # Envía email al médico
```

**Email de alerta:**
```
🚨 ALERTA CRÍTICA

Paciente: María González
Indicador: ARR
Valor: 0.25
Estado: CRÍTICO

Justificación:
ARR de 0.25 supera umbral de 0.20...

Acción requerida: Revisar caso inmediatamente.
```

### Consulta a IAs via n8n

En la página de **Consulta IA**, verás un checkbox:

```
☑️ Usar n8n para consulta (recomendado si está configurado)
```

Si está marcado:
```python
# Streamlit prepara el prompt
prompt = "Paciente de 35 años con EM..."

# Envía a n8n
n8n_client.consultar_ias(prompt)
# ↓
# n8n consulta DeepSeek y Copilot en paralelo
# ↓
# Devuelve ambos resultados
# ↓
# Streamlit muestra comparación
```

---

## ⚙️ Configuración

### Paso 1: Instalar n8n

```bash
# Opción 1: npm
npm install -g n8n

# Opción 2: Docker
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n
```

### Paso 2: Iniciar n8n

```bash
n8n start
```

Abre: http://localhost:5678

### Paso 3: Importar Workflows

1. En n8n, ve a **Workflows** → **Import from File**
2. Importa estos 3 archivos:
   - `n8n/workflows/ai_orchestration.json`
   - `n8n/workflows/critical_alerts.json`
   - `n8n/workflows/appointment_reminders.json`

### Paso 4: Configurar Variables de Entorno en n8n

En n8n, ve a **Settings** → **Environments**:

```env
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx
COPILOT_API_KEY=sk-xxxxxxxxxxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Paso 5: Configurar SMTP (para emails)

En n8n, ve a **Credentials** → **Create New** → **SMTP**:

```
Host: smtp.gmail.com
Port: 587
User: tu-email@gmail.com
Password: tu-app-password
Secure: TLS
```

### Paso 6: Activar Workflows

1. Abre cada workflow en n8n
2. Click en el toggle **Active** (arriba a la derecha)
3. Verifica que esté en verde ✅

### Paso 7: Configurar Streamlit

Agrega a tu `.env`:

```env
# n8n Webhooks
N8N_AI_WEBHOOK=http://localhost:5678/webhook/ai-consultation
N8N_ALERT_WEBHOOK=http://localhost:5678/webhook/critical-alert
```

### Paso 8: Reiniciar Streamlit

```bash
# Detén la app (Ctrl+C)
streamlit run app.py
```

---

## 🧪 Probar la Integración

### Test 1: Alerta Crítica

1. Ve a **Indicadores Clínicos**
2. Ingresa datos que generen un indicador crítico:
   - Recaídas: 2
   - Lesiones T1 Gd+: 5
   - EDSS actual: 5.0 (si basal es 3.0)
3. Click en **Calcular Indicadores**
4. Deberías ver: `🔔 Alerta enviada para indicador crítico: ARR`
5. Revisa tu email configurado en n8n

### Test 2: Consulta IA via n8n

1. Ve a **Consulta IA**
2. Marca el checkbox: `☑️ Usar n8n para consulta`
3. Click en **CONSULTAR A LAS IAs**
4. Espera 10-30 segundos
5. Deberías ver: `✅ Consulta completada via n8n!`
6. Compara los diagnósticos de DeepSeek y Copilot

### Test 3: Recordatorios Automáticos

Este workflow se ejecuta automáticamente todos los días a las 9:00 AM.

Para probarlo manualmente:
1. Abre el workflow en n8n
2. Click en **Execute Workflow** (botón de play)
3. Revisa los emails enviados

---

## 📊 Monitoreo

### Ver Ejecuciones en n8n

1. Ve a **Executions** en n8n
2. Verás todas las ejecuciones de workflows
3. Click en una ejecución para ver detalles
4. Errores se muestran en rojo 🔴

### Logs en Streamlit

Los logs se guardan en `logs/app.log`:

```bash
tail -f logs/app.log
```

Busca líneas como:
```
INFO - Alerta crítica enviada para María González
INFO - Consulta IA exitosa via n8n
```

---

## 🔧 Troubleshooting

### Error: "N8N_AI_WEBHOOK no configurado"

**Solución:**
1. Verifica que `.env` tenga las variables de n8n
2. Reinicia Streamlit

### Error: "Timeout al consultar IAs via n8n"

**Solución:**
1. Verifica que n8n esté corriendo: http://localhost:5678
2. Verifica que los workflows estén activos (verde)
3. Aumenta el timeout en `src/n8n/n8n_client.py` si es necesario

### Error: "Authentication failed" en n8n

**Solución:**
1. Verifica las API keys en n8n Settings → Environments
2. Asegúrate de usar el formato correcto: `Bearer sk-xxxxx`

### Emails no se envían

**Solución:**
1. Verifica credenciales SMTP en n8n
2. Si usas Gmail, activa "App Passwords"
3. Revisa spam/correo no deseado
4. Verifica que el email en el workflow sea correcto

---

## 📈 Ventajas de Usar n8n

### ✅ Con n8n:
- Consultas paralelas más eficientes
- Monitoreo centralizado de todas las ejecuciones
- Logs detallados de cada paso
- Fácil de modificar workflows sin cambiar código
- Alertas automáticas por email
- Recordatorios programados
- Escalable para múltiples usuarios

### ⚠️ Sin n8n:
- Funciona igual pero sin automatización
- No hay alertas por email
- No hay recordatorios automáticos
- Menos monitoreo

---

## 🎯 Próximos Pasos

1. ✅ Instala n8n
2. ✅ Importa los 3 workflows
3. ✅ Configura variables de entorno en n8n
4. ✅ Configura SMTP para emails
5. ✅ Activa los workflows
6. ✅ Agrega las URLs a tu `.env`
7. ✅ Reinicia Streamlit
8. ✅ Prueba la integración

**¡La integración está lista para usar! 🚀**

---

## 📝 Notas

- n8n es **opcional** - la app funciona sin él
- Si n8n no está configurado, se usa el método directo
- Los workflows están optimizados y listos para producción
- Puedes personalizar los workflows en n8n según tus necesidades
