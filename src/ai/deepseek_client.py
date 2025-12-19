"""
Cliente para DeepSeek API
"""
import os
import httpx
from typing import Dict, Any, Optional
from decimal import Decimal
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential
from config import AIConfig

class DeepSeekClient:
    """Cliente para interactuar con DeepSeek API"""
    
    def __init__(self):
        # Intentar leer de Streamlit secrets primero (para Streamlit Cloud)
        # Si no existe, usar variables de entorno (para desarrollo local)
        try:
            import streamlit as st
            self.api_key = st.secrets.get("DEEPSEEK_API_KEY")
            self.api_url = st.secrets.get("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
        except:
            # Fallback a variables de entorno locales
            self.api_key = os.getenv("DEEPSEEK_API_KEY")
            self.api_url = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
        
        if not self.api_key:
            logger.warning("DEEPSEEK_API_KEY no configurada")
    
    @retry(
        stop=stop_after_attempt(AIConfig.MAX_RETRIES),
        wait=wait_exponential(multiplier=AIConfig.RETRY_DELAY, min=2, max=10)
    )
    async def query(
        self,
        prompt: str,
        temperature: float = AIConfig.DEEPSEEK_TEMPERATURE,
        max_tokens: int = AIConfig.DEEPSEEK_MAX_TOKENS
    ) -> Dict[str, Any]:
        """
        Realiza una consulta a DeepSeek API
        
        Args:
            prompt: Prompt médico a enviar
            temperature: Temperatura para generación (0-1)
            max_tokens: Máximo de tokens en respuesta
            
        Returns:
            Diccionario con respuesta de la IA
        """
        try:
            if not self.api_key:
                raise ValueError("DEEPSEEK_API_KEY no configurada")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": AIConfig.DEEPSEEK_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un neurólogo experto en Esclerosis Múltiple con más de 20 años de experiencia."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            logger.info("Enviando consulta a DeepSeek API")
            
            async with httpx.AsyncClient(timeout=AIConfig.API_TIMEOUT) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                
                data = response.json()
                
                # Extraer respuesta
                diagnostico = data['choices'][0]['message']['content']
                
                # Extraer nivel de confianza del texto
                confianza = self._extract_confidence(diagnostico)
                
                logger.info(f"Respuesta recibida de DeepSeek (confianza: {confianza})")
                
                return {
                    'diagnostico': diagnostico,
                    'confianza': confianza,
                    'tokens_used': data.get('usage', {}).get('total_tokens', 0)
                }
                
        except httpx.HTTPStatusError as e:
            logger.error(f"Error HTTP en DeepSeek API: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error en consulta a DeepSeek: {e}")
            raise
    
    def _extract_confidence(self, text: str) -> Decimal:
        """
        Extrae el nivel de confianza del texto de diagnóstico
        
        Args:
            text: Texto del diagnóstico
            
        Returns:
            Nivel de confianza (0-10)
        """
        import re
        
        # Buscar patrones como "Nivel de confianza: 8/10" o "Confianza: 8"
        patterns = [
            r'[Nn]ivel de confianza[:\s]+(\d+(?:\.\d+)?)\s*/?\s*10',
            r'[Cc]onfianza[:\s]+(\d+(?:\.\d+)?)\s*/?\s*10',
            r'[Cc]onfianza[:\s]+(\d+(?:\.\d+)?)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    confianza = Decimal(match.group(1))
                    # Asegurar que esté en rango 0-10
                    if 0 <= confianza <= 10:
                        return confianza
                except:
                    continue
        
        # Si no se encuentra, retornar valor por defecto
        logger.warning("No se pudo extraer nivel de confianza, usando valor por defecto: 7.0")
        return Decimal('7.0')
    
    async def test_connection(self) -> bool:
        """
        Prueba la conexión con DeepSeek API
        
        Returns:
            True si la conexión es exitosa
        """
        try:
            result = await self.query(
                "Responde solo con 'OK' si recibes este mensaje.",
                max_tokens=10
            )
            return 'OK' in result['diagnostico'] or result['diagnostico'] is not None
        except Exception as e:
            logger.error(f"Error al probar conexión con DeepSeek: {e}")
            return False
