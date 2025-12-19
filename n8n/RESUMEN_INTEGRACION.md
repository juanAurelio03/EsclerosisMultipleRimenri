# ✅ Integración n8n Completada

## 📋 Resumen de Cambios

He integrado completamente los workflows de n8n con tu aplicación Streamlit.

### Archivos Creados:
1. ✅ `src/n8n/n8n_client.py` - Cliente para webhooks de n8n
2. ✅ `src/n8n/__init__.py` - Módulo n8n
3. ✅ `n8n/INTEGRACION_STREAMLIT.md` - Guía completa de integración

### Archivos Modificados:
1. ✅ `pages/3_🔬_Indicadores_Clínicos.py` - Alertas críticas automáticas
2. ✅ `pages/4_🤖_Consulta_IA.py` - Opción de usar n8n
3. ✅ `.env.example` - Variables de n8n agregadas

---

## 🎯 Funcionalidades Agregadas

### 1. Alertas Críticas Automáticas

**Cuándo:** Al calcular indicadores clínicos

**Qué hace:**
- Detecta automáticamente indicadores críticos (🔴)
- Envía webhook a n8n
- n8n formatea y envía email de alerta al médico

**Ejemplo:**
```
Calculas indicadores → ARR = 0.25 (crítico)
↓
Se envía automáticamente a n8n
↓
Email al médico: "🚨 ALERTA CRÍTICA - ARR"
```

### 2. Consulta IA via n8n

**Cuándo:** En la página de Consulta IA

**Qué hace:**
- Checkbox para elegir usar n8n
- Si está marcado, usa n8n como orquestador
- n8n consulta DeepSeek y Copilot en paralelo
- Devuelve ambos resultados para comparación

**Ventajas:**
- Más eficiente
- Monitoreo centralizado en n8n
- Logs detallados de cada consulta

---

## ⚙️ Configuración Rápida

### Opción A: Sin n8n (funciona ahora mismo)
Tu app ya funciona sin n8n. Las consultas IA se hacen directamente.

### Opción B: Con n8n (recomendado)

**1. Instalar n8n:**
```bash
npm install -g n8n
```

**2. Iniciar n8n:**
```bash
n8n start
```

**3. Importar workflows:**
- Abre http://localhost:5678
- Importa los 3 archivos de `n8n/workflows/`

**4. Configurar en n8n:**
- Settings → Environments:
  ```
  DEEPSEEK_API_KEY=tu_key
  COPILOT_API_KEY=tu_key
  SUPABASE_URL=tu_url
  SUPABASE_KEY=tu_key
  ```
- Credentials → SMTP (para emails)

**5. Activar workflows:**
- Abre cada workflow
- Click en toggle "Active"

**6. Agregar a tu `.env`:**
```env
N8N_AI_WEBHOOK=http://localhost:5678/webhook/ai-consultation
N8N_ALERT_WEBHOOK=http://localhost:5678/webhook/critical-alert
```

**7. Reiniciar Streamlit:**
```bash
streamlit run app.py
```

---

## 🧪 Probar

### Test Alerta Crítica:
1. Ve a Indicadores Clínicos
2. Ingresa: Recaídas = 2, Lesiones T1 = 5
3. Calcula indicadores
4. Verás: `🔔 Alerta enviada para indicador crítico`
5. Revisa tu email

### Test Consulta IA:
1. Ve a Consulta IA
2. Marca: `☑️ Usar n8n para consulta`
3. Click "CONSULTAR A LAS IAs"
4. Verás: `✅ Consulta completada via n8n!`

---

## 📚 Documentación

Lee `n8n/INTEGRACION_STREAMLIT.md` para:
- Guía completa de configuración
- Troubleshooting
- Monitoreo
- Personalización de workflows

---

## 🎉 ¡Listo!

Tu aplicación ahora tiene:
- ✅ Alertas críticas automáticas por email
- ✅ Consulta IA via n8n (opcional)
- ✅ Recordatorios de citas programados (9:00 AM diario)
- ✅ Monitoreo centralizado en n8n
- ✅ Funciona con o sin n8n

**Próximos pasos:** Lee `INTEGRACION_STREAMLIT.md` para configurar n8n.
