"""
Motor de cálculo de indicadores clínicos
"""
from typing import Tuple, Dict, Any
from decimal import Decimal
from datetime import datetime, timedelta
from config import (
    IndicatorRanges,
    EstadoIndicador,
    JustificationMessages,
    SystemConstants
)
from loguru import logger

class IndicatorCalculator:
    """Calculadora de indicadores clínicos para Esclerosis Múltiple"""
    
    @staticmethod
    def calculate_arr(
        total_recaidas: int,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> Tuple[Decimal, EstadoIndicador, str]:
        """
        Calcula la Tasa Anualizada de Recaídas (ARR)
        
        Args:
            total_recaidas: Número total de recaídas en el período
            fecha_inicio: Fecha de inicio del período
            fecha_fin: Fecha de fin del período
            
        Returns:
            Tupla (valor_arr, estado, justificacion)
        """
        try:
            # Calcular años-paciente
            delta = fecha_fin - fecha_inicio
            anos_paciente = delta.total_seconds() / (365.25 * 24 * 60 * 60)
            
            # Evitar división por cero
            if anos_paciente == 0:
                anos_paciente = 1
            
            # Calcular ARR
            arr = Decimal(str(total_recaidas / anos_paciente))
            arr = arr.quantize(Decimal('0.01'))
            
            # Clasificar según rangos
            estado = IndicatorCalculator._classify_value(
                float(arr),
                IndicatorRanges.ARR_RANGES
            )
            
            # Generar justificación
            justificacion = JustificationMessages.ARR[estado.value].format(valor=arr)
            
            logger.info(f"ARR calculado: {arr} - Estado: {estado.value}")
            return arr, estado, justificacion
            
        except Exception as e:
            logger.error(f"Error al calcular ARR: {e}")
            raise
    
    @staticmethod
    def classify_t1_gd(conteo_lesiones: int) -> Tuple[EstadoIndicador, str]:
        """
        Clasifica lesiones T1 con gadolinio
        
        Args:
            conteo_lesiones: Número de lesiones T1 Gd+
            
        Returns:
            Tupla (estado, justificacion)
        """
        try:
            estado = IndicatorCalculator._classify_value(
                conteo_lesiones,
                IndicatorRanges.T1_GD_RANGES
            )
            
            justificacion = JustificationMessages.T1_GD[estado.value].format(
                valor=conteo_lesiones
            )
            
            logger.info(f"T1 Gd+ clasificado: {conteo_lesiones} - Estado: {estado.value}")
            return estado, justificacion
            
        except Exception as e:
            logger.error(f"Error al clasificar T1 Gd+: {e}")
            raise
    
    @staticmethod
    def calculate_t2_difference(
        t2_actual: int,
        t2_previo: int
    ) -> Tuple[int, EstadoIndicador, str]:
        """
        Calcula diferencia de lesiones T2
        
        Args:
            t2_actual: Conteo actual de lesiones T2
            t2_previo: Conteo previo de lesiones T2
            
        Returns:
            Tupla (diferencia, estado, justificacion)
        """
        try:
            diferencia = t2_actual - t2_previo
            
            estado = IndicatorCalculator._classify_value(
                diferencia,
                IndicatorRanges.T2_NUEVAS_RANGES
            )
            
            justificacion = JustificationMessages.T2_NUEVAS[estado.value].format(
                valor=diferencia
            )
            
            logger.info(f"T2 diferencia calculada: {diferencia} - Estado: {estado.value}")
            return diferencia, estado, justificacion
            
        except Exception as e:
            logger.error(f"Error al calcular diferencia T2: {e}")
            raise
    
    @staticmethod
    def evaluate_cdp12(
        edss_basal: Decimal,
        edss_actual: Decimal
    ) -> Tuple[Decimal, bool, EstadoIndicador, str]:
        """
        Evalúa Confirmed Disability Progression a 12 semanas
        
        Args:
            edss_basal: EDSS basal del paciente
            edss_actual: EDSS actual
            
        Returns:
            Tupla (delta_edss, progresion_confirmada, estado, justificacion)
        """
        try:
            delta = edss_actual - edss_basal
            
            # Determinar umbral según EDSS basal
            if edss_basal <= Decimal(str(SystemConstants.CDP12_EDSS_THRESHOLD)):
                umbral = Decimal(str(SystemConstants.CDP12_UMBRAL_BAJO))
            else:
                umbral = Decimal(str(SystemConstants.CDP12_UMBRAL_ALTO))
            
            # Evaluar progresión
            progresion = delta >= umbral
            
            # Determinar estado
            if progresion:
                estado = EstadoIndicador.CRITICO
                justificacion = JustificationMessages.CDP12['critico'].format(
                    delta=delta,
                    umbral=umbral,
                    basal=edss_basal
                )
            elif delta > 0:
                estado = EstadoIndicador.ALERTA
                justificacion = JustificationMessages.CDP12['alerta'].format(
                    delta=delta,
                    umbral=umbral
                )
            else:
                estado = EstadoIndicador.NORMAL
                justificacion = JustificationMessages.CDP12['normal'].format(
                    delta=delta
                )
            
            logger.info(f"CDP-12 evaluado: ΔEDSS={delta}, Progresión={progresion}")
            return delta, progresion, estado, justificacion
            
        except Exception as e:
            logger.error(f"Error al evaluar CDP-12: {e}")
            raise
    
    @staticmethod
    def evaluate_neda3(
        sin_recaidas: bool,
        sin_lesiones_rm: bool,
        sin_progresion_edss: bool
    ) -> Tuple[bool, EstadoIndicador, str, Dict[str, bool]]:
        """
        Evalúa cumplimiento de NEDA-3
        
        Args:
            sin_recaidas: Si no hubo recaídas
            sin_lesiones_rm: Si no hubo nuevas lesiones en RM
            sin_progresion_edss: Si no hubo progresión de EDSS
            
        Returns:
            Tupla (cumple_neda3, estado, justificacion, detalles)
        """
        try:
            cumple = sin_recaidas and sin_lesiones_rm and sin_progresion_edss
            
            detalles = {
                'sin_recaidas': sin_recaidas,
                'sin_lesiones_rm': sin_lesiones_rm,
                'sin_progresion_edss': sin_progresion_edss
            }
            
            if cumple:
                estado = EstadoIndicador.NORMAL
                justificacion = JustificationMessages.NEDA3['normal']
            else:
                estado = EstadoIndicador.CRITICO
                
                # Construir detalles de criterios no cumplidos
                criterios_no_cumplidos = []
                if not sin_recaidas:
                    criterios_no_cumplidos.append("(1) Presencia de recaídas")
                if not sin_lesiones_rm:
                    criterios_no_cumplidos.append("(2) Nuevas lesiones en RM")
                if not sin_progresion_edss:
                    criterios_no_cumplidos.append("(3) Progresión de EDSS")
                
                detalles_texto = ", ".join(criterios_no_cumplidos)
                justificacion = JustificationMessages.NEDA3['critico'].format(
                    detalles=detalles_texto
                )
            
            logger.info(f"NEDA-3 evaluado: Cumple={cumple}")
            return cumple, estado, justificacion, detalles
            
        except Exception as e:
            logger.error(f"Error al evaluar NEDA-3: {e}")
            raise
    
    @staticmethod
    def _classify_value(
        valor: float,
        rangos: Dict[str, Tuple[float, float]]
    ) -> EstadoIndicador:
        """
        Clasifica un valor según rangos definidos
        
        Args:
            valor: Valor a clasificar
            rangos: Diccionario de rangos {estado: (min, max)}
            
        Returns:
            EstadoIndicador correspondiente
        """
        if rangos['normal'][0] <= valor <= rangos['normal'][1]:
            return EstadoIndicador.NORMAL
        elif rangos['alerta'][0] <= valor <= rangos['alerta'][1]:
            return EstadoIndicador.ALERTA
        else:
            return EstadoIndicador.CRITICO
