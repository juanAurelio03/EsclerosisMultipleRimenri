"""
Orquestador de consulta dual a IAs (DeepSeek + Microsoft Copilot)
"""
import asyncio
from typing import Dict, Any, Optional, Tuple
from decimal import Decimal
from loguru import logger

from .deepseek_client import DeepSeekClient
from .copilot_client import CopilotClient
from .prompt_builder import MedicalPromptBuilder
from src.database import db

class DualAIConsultation:
    """Orquestador para consultas paralelas a ambas IAs"""
    
    def __init__(self):
        self.deepseek = DeepSeekClient()
        self.copilot = CopilotClient()
        self.prompt_builder = MedicalPromptBuilder()
    
    def _prepare_context_sync(
        self,
        paciente_id: str,
        cita_id: str
    ) -> Dict[str, Any]:
        """
        Prepara el contexto completo para la consulta a las IAs (Versión síncrona)
        
        Args:
            paciente_id: ID del paciente
            cita_id: ID de la cita actual
            
        Returns:
            Diccionario con todo el contexto necesario
        """
        try:
            logger.info(f"Preparando contexto para paciente {paciente_id}, cita {cita_id}")
            
            # Obtener datos del paciente
            paciente = db.obtener_paciente(paciente_id)
            if not paciente:
                raise ValueError(f"Paciente {paciente_id} no encontrado")
            
            # Obtener cita actual
            cita = db.obtener_cita(cita_id)
            if not cita:
                raise ValueError(f"Cita {cita_id} no encontrada")
            
            # Obtener indicadores de la cita actual
            indicadores_actuales = db.obtener_indicadores_cita(cita_id)
            
            # Obtener EDSS actual de los indicadores
            edss_actual = paciente.get('edss_basal')  # Por defecto
            for ind in indicadores_actuales:
                if ind.get('indicador_tipo') == 'CDP12':
                    variables = ind.get('variables_entrada', {})
                    if 'edss_actual' in variables:
                        edss_actual = Decimal(str(variables['edss_actual']))
                        break
            
            # Obtener historial de citas anteriores
            todas_citas = db.listar_citas_paciente(paciente_id)
            
            # Filtrar citas anteriores a la actual y obtener sus indicadores
            historial_citas = []
            for c in todas_citas:
                if c['id'] != cita_id and c.get('estado') == 'completada':
                    indicadores = db.obtener_indicadores_cita(c['id'])
                    historial_citas.append({
                        **c,
                        'indicadores': indicadores
                    })
            
            # Ordenar por fecha
            historial_citas.sort(key=lambda x: x.get('fecha_cita', ''))
            
            context = {
                'paciente': paciente,
                'cita': cita,
                'indicadores_actuales': indicadores_actuales,
                'edss_actual': edss_actual,
                'historial_citas': historial_citas
            }
            
            logger.info("Contexto preparado exitosamente")
            return context
            
        except Exception as e:
            logger.error(f"Error al preparar contexto: {e}")
            raise

    async def prepare_context(
        self,
        paciente_id: str,
        cita_id: str
    ) -> Dict[str, Any]:
        """
        Prepara el contexto completo para la consulta a las IAs
        
        Args:
            paciente_id: ID del paciente
            cita_id: ID de la cita actual
            
        Returns:
            Diccionario con todo el contexto necesario
        """
        return self._prepare_context_sync(paciente_id, cita_id)

    def _build_prompt(self, paciente_id: str, cita_id: str) -> str:
        """
        Construye el prompt para n8n (Método síncrono)
        
        Args:
            paciente_id: ID del paciente
            cita_id: ID de la cita
            
        Returns:
            Prompt completo como string
        """
        context = self._prepare_context_sync(paciente_id, cita_id)
        
        return self.prompt_builder.build_complete_prompt(
            paciente=context['paciente'],
            indicadores_actuales=context['indicadores_actuales'],
            edss_actual=context['edss_actual'],
            historial_citas=context['historial_citas']
        )
    
    async def query_both_ais(
        self,
        paciente_id: str,
        cita_id: str
    ) -> Dict[str, Any]:
        """
        Realiza consultas paralelas a ambas IAs
        
        Args:
            paciente_id: ID del paciente
            cita_id: ID de la cita
            
        Returns:
            Diccionario con respuestas de ambas IAs
        """
        try:
            logger.info("Iniciando consulta dual a IAs")
            
            # Preparar contexto
            context = await self.prepare_context(paciente_id, cita_id)
            
            # Construir prompt
            prompt = self.prompt_builder.build_complete_prompt(
                paciente=context['paciente'],
                indicadores_actuales=context['indicadores_actuales'],
                edss_actual=context['edss_actual'],
                historial_citas=context['historial_citas']
            )
            
            # Realizar consultas en paralelo
            logger.info("Enviando consultas paralelas a DeepSeek y Copilot")
            
            results = await asyncio.gather(
                self._query_deepseek_safe(prompt),
                self._query_copilot_safe(prompt),
                return_exceptions=True
            )
            
            deepseek_result, copilot_result = results
            
            # Procesar resultados
            response = {
                'cita_id': cita_id,
                'paciente_id': paciente_id,
                'deepseek': self._process_result(deepseek_result, 'DeepSeek'),
                'copilot': self._process_result(copilot_result, 'Copilot'),
                'prompt_usado': prompt
            }
            
            logger.info("Consulta dual completada")
            return response
            
        except Exception as e:
            logger.error(f"Error en consulta dual: {e}")
            raise
    
    async def _query_deepseek_safe(self, prompt: str) -> Dict[str, Any]:
        """Consulta a DeepSeek con manejo de errores"""
        try:
            return await self.deepseek.query(prompt)
        except Exception as e:
            logger.error(f"Error en consulta a DeepSeek: {e}")
            return {
                'diagnostico': f"Error al consultar DeepSeek: {str(e)}",
                'confianza': Decimal('0'),
                'error': True
            }
    
    async def _query_copilot_safe(self, prompt: str) -> Dict[str, Any]:
        """Consulta a Copilot con manejo de errores"""
        try:
            return await self.copilot.query(prompt)
        except Exception as e:
            logger.error(f"Error en consulta a Copilot: {e}")
            return {
                'diagnostico': f"Error al consultar Copilot: {str(e)}",
                'confianza': Decimal('0'),
                'error': True
            }
    
    def _process_result(self, result: Any, ia_name: str) -> Dict[str, Any]:
        """Procesa el resultado de una IA"""
        if isinstance(result, Exception):
            logger.error(f"Excepción en {ia_name}: {result}")
            return {
                'diagnostico': f"Error: {str(result)}",
                'confianza': Decimal('0'),
                'error': True
            }
        elif isinstance(result, dict) and result.get('error'):
            return result
        else:
            return {
                'diagnostico': result.get('diagnostico', 'Sin respuesta'),
                'confianza': result.get('confianza', Decimal('0')),
                'tokens_used': result.get('tokens_used', 0),
                'error': False
            }
    
    def compare_responses(
        self,
        deepseek_response: Dict[str, Any],
        copilot_response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compara las respuestas de ambas IAs
        
        Args:
            deepseek_response: Respuesta de DeepSeek
            copilot_response: Respuesta de Copilot
            
        Returns:
            Análisis comparativo
        """
        try:
            # Extraer diagnósticos
            diag_deepseek = deepseek_response.get('diagnostico', '')
            diag_copilot = copilot_response.get('diagnostico', '')
            
            # Calcular similitud básica (longitud)
            len_deepseek = len(diag_deepseek.split())
            len_copilot = len(diag_copilot.split())
            
            # Comparar niveles de confianza
            conf_deepseek = float(deepseek_response.get('confianza', 0))
            conf_copilot = float(copilot_response.get('confianza', 0))
            
            comparison = {
                'longitud_deepseek': len_deepseek,
                'longitud_copilot': len_copilot,
                'confianza_deepseek': conf_deepseek,
                'confianza_copilot': conf_copilot,
                'diferencia_confianza': abs(conf_deepseek - conf_copilot),
                'ia_mas_confiada': 'DeepSeek' if conf_deepseek > conf_copilot else 'Copilot'
            }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error al comparar respuestas: {e}")
            return {}
    
    def save_results(
        self,
        cita_id: str,
        deepseek_response: Dict[str, Any],
        copilot_response: Dict[str, Any],
        ia_seleccionada: str,
        diagnostico_medico: Optional[str] = None,
        justificacion: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Guarda los resultados de la consulta dual en la base de datos
        
        Args:
            cita_id: ID de la cita
            deepseek_response: Respuesta de DeepSeek
            copilot_response: Respuesta de Copilot
            ia_seleccionada: IA seleccionada por el médico
            diagnostico_medico: Diagnóstico propio del médico (opcional)
            justificacion: Justificación de la selección (opcional)
            
        Returns:
            Registro guardado
        """
        try:
            datos = {
                'cita_id': cita_id,
                'diagnostico_deepseek': deepseek_response.get('diagnostico'),
                'confianza_deepseek': deepseek_response.get('confianza'),
                'diagnostico_copilot': copilot_response.get('diagnostico'),
                'confianza_copilot': copilot_response.get('confianza'),
                'ia_seleccionada': ia_seleccionada,
                'diagnostico_medico_override': diagnostico_medico,
                'justificacion_medico': justificacion
            }
            
            result = db.guardar_diagnostico_ia(datos)
            logger.info(f"Diagnóstico IA guardado para cita {cita_id}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error al guardar resultados: {e}")
            raise
