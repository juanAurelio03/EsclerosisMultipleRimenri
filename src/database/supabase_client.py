"""
Cliente de Supabase para gestión de base de datos
"""
import os
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from dotenv import load_dotenv
from supabase import create_client, Client
from loguru import logger
import json

# Cargar variables de entorno
load_dotenv()

class SupabaseClient:
    """Cliente singleton para interactuar con Supabase"""
    
    _instance: Optional['SupabaseClient'] = None
    _client: Optional[Client] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa el cliente de Supabase"""
        try:
            url = os.getenv("SUPABASE_URL")
            # Usar SERVICE_KEY para tener permisos completos y bypassear RLS
            key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")
            
            if not url or not key:
                raise ValueError("SUPABASE_URL y SUPABASE_SERVICE_KEY deben estar configurados en .env")
            
            self._client = create_client(url, key)
            logger.info("Cliente de Supabase inicializado correctamente con service_role key")
        except Exception as e:
            logger.error(f"Error al inicializar cliente de Supabase: {e}")
            raise
    
    @property
    def client(self) -> Client:
        """Retorna el cliente de Supabase"""
        if self._client is None:
            self._initialize_client()
        return self._client
    
    # =====================================================
    # OPERACIONES CRUD - PACIENTES
    # =====================================================
    
    def crear_paciente(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo paciente"""
        try:
            response = self.client.table('pacientes').insert(datos).execute()
            logger.info(f"Paciente creado: {datos.get('nombre_completo')}")
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error al crear paciente: {e}")
            raise
    
    def obtener_paciente(self, paciente_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un paciente por ID"""
        try:
            response = self.client.table('pacientes').select('*').eq('id', paciente_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error al obtener paciente: {e}")
            raise
    
    def listar_pacientes(self, activos_solo: bool = True) -> List[Dict[str, Any]]:
        """Lista todos los pacientes"""
        try:
            query = self.client.table('pacientes').select('*')
            if activos_solo:
                query = query.eq('activo', True)
            response = query.order('nombre_completo').execute()
            return response.data
        except Exception as e:
            logger.error(f"Error al listar pacientes: {e}")
            raise
    
    def actualizar_paciente(self, paciente_id: str, datos: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza un paciente"""
        try:
            response = self.client.table('pacientes').update(datos).eq('id', paciente_id).execute()
            logger.info(f"Paciente actualizado: {paciente_id}")
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error al actualizar paciente: {e}")
            raise
    
    # =====================================================
    # OPERACIONES CRUD - CITAS
    # =====================================================
    
    def crear_cita(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una nueva cita"""
        try:
            # Obtener el siguiente número de visita
            paciente_id = datos.get('paciente_id')
            response = self.client.table('citas')\
                .select('numero_visita')\
                .eq('paciente_id', paciente_id)\
                .order('numero_visita', desc=True)\
                .limit(1)\
                .execute()
            
            ultimo_numero = response.data[0]['numero_visita'] if response.data else 0
            datos['numero_visita'] = ultimo_numero + 1
            
            response = self.client.table('citas').insert(datos).execute()
            logger.info(f"Cita creada para paciente {paciente_id}, visita #{datos['numero_visita']}")
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error al crear cita: {e}")
            raise
    
    def obtener_cita(self, cita_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una cita por ID"""
        try:
            response = self.client.table('citas').select('*').eq('id', cita_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error al obtener cita: {e}")
            raise
    
    def listar_citas_paciente(self, paciente_id: str) -> List[Dict[str, Any]]:
        """Lista todas las citas de un paciente"""
        try:
            response = self.client.table('citas')\
                .select('*')\
                .eq('paciente_id', paciente_id)\
                .order('fecha_cita', desc=True)\
                .execute()
            return response.data
        except Exception as e:
            logger.error(f"Error al listar citas: {e}")
            raise
    
    def actualizar_cita(self, cita_id: str, datos: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza una cita"""
        try:
            response = self.client.table('citas').update(datos).eq('id', cita_id).execute()
            logger.info(f"Cita actualizada: {cita_id}")
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error al actualizar cita: {e}")
            raise
    
    def obtener_citas_pendientes(self, dias_adelante: int = 2) -> List[Dict[str, Any]]:
        """Obtiene citas pendientes en los próximos N días"""
        try:
            from datetime import timedelta
            fecha_limite = (datetime.now() + timedelta(days=dias_adelante)).isoformat()
            
            response = self.client.table('citas')\
                .select('*, pacientes(*)')\
                .eq('estado', 'pendiente')\
                .lte('fecha_cita', fecha_limite)\
                .execute()
            return response.data
        except Exception as e:
            logger.error(f"Error al obtener citas pendientes: {e}")
            raise
    
    # =====================================================
    # OPERACIONES CRUD - INDICADORES
    # =====================================================
    
    def guardar_indicador(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """Guarda un indicador clínico"""
        try:
            # Usar upsert con on_conflict para actualizar si ya existe la combinación (cita_id, indicador_tipo)
            response = self.client.table('indicadores_cita').upsert(
                datos,
                on_conflict='cita_id,indicador_tipo'
            ).execute()
            logger.info(f"Indicador guardado: {datos.get('indicador_tipo')} para cita {datos.get('cita_id')}")
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error al guardar indicador: {e}")
            raise
    
    def obtener_indicadores_cita(self, cita_id: str) -> List[Dict[str, Any]]:
        """Obtiene todos los indicadores de una cita"""
        try:
            response = self.client.table('indicadores_cita')\
                .select('*')\
                .eq('cita_id', cita_id)\
                .execute()
            return response.data
        except Exception as e:
            logger.error(f"Error al obtener indicadores: {e}")
            raise
    
    def eliminar_indicadores_cita(self, cita_id: str) -> bool:
        """Elimina todos los indicadores de una cita (útil para recalcular desde cero)"""
        try:
            response = self.client.table('indicadores_cita')\
                .delete()\
                .eq('cita_id', cita_id)\
                .execute()
            logger.info(f"Indicadores eliminados para cita {cita_id}")
            return True
        except Exception as e:
            logger.error(f"Error al eliminar indicadores: {e}")
            raise

    
    def obtener_historial_indicadores(self, paciente_id: str, tipo_indicador: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtiene historial de indicadores de un paciente"""
        try:
            query = self.client.table('indicadores_cita')\
                .select('*, citas!inner(fecha_cita, paciente_id, id)')\
                .eq('citas.paciente_id', paciente_id)
            
            if tipo_indicador:
                query = query.eq('indicador_tipo', tipo_indicador)
            
            response = query.execute()
            
            # Ordenar manualmente por fecha_cita después de obtener los datos
            if response.data:
                response.data.sort(key=lambda x: x.get('citas', {}).get('fecha_cita', ''))
            
            return response.data
        except Exception as e:
            logger.error(f"Error al obtener historial de indicadores: {e}")
            raise
    
    # =====================================================
    # OPERACIONES CRUD - DIAGNÓSTICOS IA
    # =====================================================
    
    def guardar_diagnostico_ia(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """Guarda un diagnóstico de IA"""
        try:
            response = self.client.table('diagnosticos_ia').upsert(datos).execute()
            logger.info(f"Diagnóstico IA guardado para cita {datos.get('cita_id')}")
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error al guardar diagnóstico IA: {e}")
            raise
    
    def obtener_diagnostico_ia(self, cita_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene el diagnóstico IA de una cita"""
        try:
            response = self.client.table('diagnosticos_ia')\
                .select('*')\
                .eq('cita_id', cita_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error al obtener diagnóstico IA: {e}")
            raise
    
    # =====================================================
    # OPERACIONES - MÉTRICAS IA
    # =====================================================
    
    def calcular_metricas_ia(self, fecha_inicio: Optional[date] = None, fecha_fin: Optional[date] = None) -> Dict[str, Any]:
        """Calcula métricas de precisión de las IAs"""
        try:
            # Llamar a la función PostgreSQL
            params = {}
            if fecha_inicio:
                params['p_fecha_inicio'] = fecha_inicio.isoformat()
            if fecha_fin:
                params['p_fecha_fin'] = fecha_fin.isoformat()
            
            response = self.client.rpc('obtener_metricas_ia', params).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error al calcular métricas IA: {e}")
            raise
    
    def guardar_metricas_ia(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """Guarda métricas de IA calculadas"""
        try:
            response = self.client.table('metricas_ia').upsert(datos).execute()
            logger.info(f"Métricas IA guardadas para fecha {datos.get('fecha_calculo')}")
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error al guardar métricas IA: {e}")
            raise
    
    def obtener_historial_metricas_ia(self, limite: int = 30) -> List[Dict[str, Any]]:
        """Obtiene historial de métricas de IA"""
        try:
            response = self.client.table('metricas_ia')\
                .select('*')\
                .order('fecha_calculo', desc=True)\
                .limit(limite)\
                .execute()
            return response.data
        except Exception as e:
            logger.error(f"Error al obtener auditoría: {e}")
            raise

# Instancia global del cliente
db = SupabaseClient()
