"""
Constructor de prompts médicos para IAs
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from decimal import Decimal
from config import MEDICAL_PROMPT_TEMPLATE
from loguru import logger

class MedicalPromptBuilder:
    """Constructor de prompts médicos estructurados para consultas a IAs"""
    
    @staticmethod
    def build_patient_context(paciente: Dict[str, Any]) -> str:
        """
        Construye el contexto del paciente
        
        Args:
            paciente: Datos del paciente
            
        Returns:
            Texto formateado con contexto del paciente
        """
        try:
            # Calcular años desde diagnóstico
            fecha_diagnostico = paciente.get('fecha_diagnostico')
            if isinstance(fecha_diagnostico, str):
                from dateutil import parser
                fecha_diagnostico = parser.parse(fecha_diagnostico).date()
            
            anos_diagnostico = (datetime.now().date() - fecha_diagnostico).days / 365.25
            
            context = {
                'edad': paciente.get('edad', 'N/A'),
                'genero': paciente.get('genero', 'N/A'),
                'tipo_em': paciente.get('tipo_em', 'N/A'),
                'anos_diagnostico': f"{anos_diagnostico:.1f}",
                'tratamiento_actual': paciente.get('tratamiento_actual', 'No especificado'),
                'edss_basal': paciente.get('edss_basal', 'N/A')
            }
            
            return context
            
        except Exception as e:
            logger.error(f"Error al construir contexto del paciente: {e}")
            raise
    
    @staticmethod
    def build_indicators_summary(indicadores: List[Dict[str, Any]]) -> str:
        """
        Construye resumen de indicadores clínicos
        
        Args:
            indicadores: Lista de indicadores de la cita actual
            
        Returns:
            Texto formateado con resumen de indicadores
        """
        try:
            summary_lines = []
            
            # Mapeo de emojis por estado
            estado_emoji = {
                'normal': '✓',
                'alerta': '⚠️',
                'critico': '🔴'
            }
            
            for ind in indicadores:
                tipo = ind.get('indicador_tipo', 'N/A')
                valor = ind.get('valor_calculado', 'N/A')
                estado = ind.get('estado', 'normal')
                emoji = estado_emoji.get(estado, '')
                
                # Formatear valor
                if valor is not None and valor != 'N/A':
                    if isinstance(valor, (int, float, Decimal)):
                        valor_str = f"{float(valor):.2f}"
                    else:
                        valor_str = str(valor)
                else:
                    valor_str = 'N/A'
                
                summary_lines.append(
                    f"- {tipo}: {valor_str} - {emoji} {estado.upper()}"
                )
            
            return "\n".join(summary_lines) if summary_lines else "No hay indicadores registrados"
            
        except Exception as e:
            logger.error(f"Error al construir resumen de indicadores: {e}")
            raise
    
    @staticmethod
    def build_evolution_history(historial: List[Dict[str, Any]], limite: int = 3) -> str:
        """
        Construye historial de evolución del paciente
        
        Args:
            historial: Lista de citas anteriores con indicadores
            limite: Número de citas anteriores a incluir
            
        Returns:
            Texto formateado con historial evolutivo
        """
        try:
            if not historial:
                return "No hay historial previo disponible (primera visita)"
            
            history_lines = []
            
            # Tomar las últimas N citas
            recent_history = historial[-limite:] if len(historial) > limite else historial
            
            for i, cita in enumerate(recent_history, 1):
                fecha = cita.get('fecha_cita', 'Fecha desconocida')
                if isinstance(fecha, str):
                    try:
                        from dateutil import parser
                        fecha = parser.parse(fecha).strftime('%Y-%m-%d')
                    except:
                        pass
                
                history_lines.append(f"\n**Visita #{cita.get('numero_visita', i)} ({fecha}):**")
                
                # Agregar indicadores de esa cita si están disponibles
                if 'indicadores' in cita and cita['indicadores']:
                    for ind in cita['indicadores']:
                        tipo = ind.get('indicador_tipo', 'N/A')
                        valor = ind.get('valor_calculado', 'N/A')
                        estado = ind.get('estado', 'normal')
                        
                        history_lines.append(f"  - {tipo}: {valor} ({estado})")
            
            return "\n".join(history_lines) if history_lines else "Historial no disponible"
            
        except Exception as e:
            logger.error(f"Error al construir historial de evolución: {e}")
            return "Error al procesar historial"
    
    @staticmethod
    def build_complete_prompt(
        paciente: Dict[str, Any],
        indicadores_actuales: List[Dict[str, Any]],
        edss_actual: Decimal,
        historial_citas: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Construye el prompt completo para enviar a las IAs
        
        Args:
            paciente: Datos del paciente
            indicadores_actuales: Indicadores de la cita actual
            edss_actual: EDSS actual del paciente
            historial_citas: Historial de citas anteriores
            
        Returns:
            Prompt completo formateado
        """
        try:
            # Construir cada sección
            patient_context = MedicalPromptBuilder.build_patient_context(paciente)
            indicators_summary = MedicalPromptBuilder.build_indicators_summary(indicadores_actuales)
            evolution_history = MedicalPromptBuilder.build_evolution_history(
                historial_citas or []
            )
            
            # Completar el template
            prompt = MEDICAL_PROMPT_TEMPLATE.format(
                edad=patient_context['edad'],
                genero=patient_context['genero'],
                tipo_em=patient_context['tipo_em'],
                anos_diagnostico=patient_context['anos_diagnostico'],
                tratamiento_actual=patient_context['tratamiento_actual'],
                edss_basal=patient_context['edss_basal'],
                edss_actual=edss_actual,
                indicadores_resumen=indicators_summary,
                historial_evolucional=evolution_history,
                contexto_pdf="No se utiliza documentación de referencia externa."
            )
            
            logger.info("Prompt médico completo construido exitosamente")
            return prompt
            
        except Exception as e:
            logger.error(f"Error al construir prompt completo: {e}")
            raise
