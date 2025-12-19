"""
Cliente para integración con n8n workflows
"""
import os
import httpx
from typing import Dict, Any, Optional
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

class N8NClient:
    """Cliente para interactuar con workflows de n8n"""
    
    def __init__(self):
        self.ai_webhook_url = os.getenv("N8N_AI_WEBHOOK", "")
        self.alert_webhook_url = os.getenv("N8N_ALERT_WEBHOOK", "")
        self.timeout = 180.0  # 3 minutos para consultas IA (los modelos pueden tardar)
        
    def is_configured(self) -> bool:
        """Verifica si n8n está configurado"""
        # Retorna True si al menos la URL de consulta IA está configurada
        return bool(self.ai_webhook_url)
    
    async def consultar_ias(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Consulta a DeepSeek y Copilot via n8n
        
        Args:
            prompt: Prompt médico para las IAs
            
        Returns:
            Dict con respuestas de ambas IAs o None si hay error
        """
        if not self.ai_webhook_url:
            logger.warning("N8N_AI_WEBHOOK no configurado")
            return None
            
        try:
            logger.info(f"Enviando consulta a n8n webhook: {self.ai_webhook_url}")
            logger.debug(f"Longitud del prompt: {len(prompt)} caracteres")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.ai_webhook_url,
                    json={"prompt": prompt}
                )
                
                logger.info(f"Respuesta HTTP status: {response.status_code}")
                logger.debug(f"Headers de respuesta: {response.headers}")
                
                response.raise_for_status()
                
                # Intentar parsear JSON
                try:
                    data = response.json()
                    logger.info(f"✅ Consulta IA exitosa via n8n")
                    logger.debug(f"Estructura de respuesta: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                    logger.debug(f"Respuesta completa: {data}")
                    return data
                except Exception as json_error:
                    logger.error(f"Error al parsear JSON de n8n: {json_error}")
                    logger.error(f"Contenido de respuesta: {response.text[:500]}")
                    return None
                
        except httpx.TimeoutException:
            logger.error(f"⏱️ Timeout al consultar IAs via n8n (>{self.timeout}s)")
            return None
        except httpx.HTTPError as e:
            logger.error(f"❌ Error HTTP al consultar IAs: {e}")
            logger.error(f"Status code: {e.response.status_code if hasattr(e, 'response') else 'N/A'}")
            logger.error(f"Response text: {e.response.text[:500] if hasattr(e, 'response') else 'N/A'}")
            return None
        except Exception as e:
            logger.error(f"❌ Error inesperado al consultar IAs: {e}")
            logger.exception(e)
            return None
    
    async def enviar_alerta_critica(
        self,
        indicador: Dict[str, Any],
        paciente: Dict[str, Any],
        cita: Dict[str, Any]
    ) -> bool:
        """
        Envía alerta crítica via n8n
        
        Args:
            indicador: Datos del indicador crítico
            paciente: Datos del paciente
            cita: Datos de la cita
            
        Returns:
            True si se envió correctamente, False si hubo error
        """
        if not self.alert_webhook_url:
            logger.warning("N8N_ALERT_WEBHOOK no configurado")
            return False
            
        try:
            payload = {
                "indicador": {
                    "tipo": indicador.get("indicador_tipo"),
                    "valor": float(indicador.get("valor_calculado", 0)),
                    "estado": indicador.get("estado"),
                    "justificacion": indicador.get("justificacion_texto")
                },
                "paciente": {
                    "nombre_completo": paciente.get("nombre_completo")
                },
                "cita": {
                    "numero_visita": cita.get("numero_visita")
                }
            }
            
            logger.info(f"📤 Intentando enviar alerta crítica a: {self.alert_webhook_url}")
            logger.debug(f"Payload: {payload}")
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    self.alert_webhook_url,
                    json=payload
                )
                
                logger.info(f"📨 Respuesta del webhook: Status {response.status_code}")
                logger.debug(f"Response body: {response.text[:200]}")
                
                response.raise_for_status()
                
                logger.info(f"✅ Alerta crítica enviada exitosamente para {paciente.get('nombre_completo')} - {indicador.get('indicador_tipo')}")
                return True
                
        except httpx.HTTPError as e:
            logger.error(f"❌ Error HTTP al enviar alerta: {e}")
            logger.error(f"Status: {e.response.status_code if hasattr(e, 'response') else 'N/A'}")
            logger.error(f"Response: {e.response.text[:500] if hasattr(e, 'response') else 'N/A'}")
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado al enviar alerta: {e}")
            logger.exception(e)
            return False

# Instancia global
n8n_client = N8NClient()
