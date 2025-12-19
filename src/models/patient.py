"""
Modelos Pydantic para validación de datos
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from config import TipoEM, EstadoCita, TipoIndicador, EstadoIndicador, IASeleccionada

# =====================================================
# MODELO: Paciente
# =====================================================

class Patient(BaseModel):
    """Modelo de paciente"""
    id: Optional[str] = None
    nombre_completo: str = Field(..., min_length=1, max_length=255)
    edad: int = Field(..., gt=0, lt=120)
    genero: str = Field(..., min_length=1, max_length=50)
    tipo_em: TipoEM
    edss_basal: Decimal = Field(..., ge=0, le=10)
    tratamiento_actual: Optional[str] = Field(None, max_length=255)
    fecha_diagnostico: date
    historial_medico: Optional[Dict[str, Any]] = Field(default_factory=dict)
    medico_asignado_id: Optional[str] = None
    activo: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @validator('edss_basal')
    def validar_edss(cls, v):
        """Valida que EDSS sea múltiplo de 0.5"""
        if float(v) % 0.5 != 0:
            raise ValueError('EDSS debe ser múltiplo de 0.5')
        return v
    
    @validator('fecha_diagnostico')
    def validar_fecha_diagnostico(cls, v):
        """Valida que la fecha de diagnóstico no sea futura"""
        if v > date.today():
            raise ValueError('La fecha de diagnóstico no puede ser futura')
        return v
    
    class Config:
        use_enum_values = True
        json_encoders = {
            Decimal: lambda v: float(v),
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }

# =====================================================
# MODELO: Cita
# =====================================================

class Appointment(BaseModel):
    """Modelo de cita"""
    id: Optional[str] = None
    paciente_id: str
    fecha_cita: datetime
    numero_visita: Optional[int] = None
    estado: EstadoCita = EstadoCita.PENDIENTE
    notas_medicas: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# =====================================================
# MODELO: Indicador Clínico
# =====================================================

class ClinicalIndicator(BaseModel):
    """Modelo de indicador clínico"""
    id: Optional[str] = None
    cita_id: str
    indicador_tipo: TipoIndicador
    valor_calculado: Optional[Decimal] = None
    estado: EstadoIndicador
    justificacion_texto: str
    variables_entrada: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[datetime] = None
    
    class Config:
        use_enum_values = True
        json_encoders = {
            Decimal: lambda v: float(v) if v is not None else None,
            datetime: lambda v: v.isoformat()
        }

# =====================================================
# MODELO: Diagnóstico IA
# =====================================================

class AIDiagnostic(BaseModel):
    """Modelo de diagnóstico de IA"""
    id: Optional[str] = None
    cita_id: str
    diagnostico_deepseek: Optional[str] = None
    confianza_deepseek: Optional[Decimal] = Field(None, ge=0, le=10)
    diagnostico_copilot: Optional[str] = None
    confianza_copilot: Optional[Decimal] = Field(None, ge=0, le=10)
    ia_seleccionada: IASeleccionada
    diagnostico_medico_override: Optional[str] = None
    justificacion_medico: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @validator('confianza_deepseek', 'confianza_copilot')
    def validar_confianza(cls, v):
        """Valida que la confianza esté entre 0 y 10"""
        if v is not None and (v < 0 or v > 10):
            raise ValueError('La confianza debe estar entre 0 y 10')
        return v
    
    class Config:
        use_enum_values = True
        json_encoders = {
            Decimal: lambda v: float(v) if v is not None else None,
            datetime: lambda v: v.isoformat()
        }

# =====================================================
# MODELO: Métricas IA
# =====================================================

class AIMetrics(BaseModel):
    """Modelo de métricas de IA"""
    id: Optional[str] = None
    fecha_calculo: date
    total_consultas: int = 0
    selecciones_deepseek: int = 0
    selecciones_copilot: int = 0
    selecciones_medico_override: int = 0
    accuracy_deepseek: Optional[Decimal] = None
    accuracy_copilot: Optional[Decimal] = None
    created_at: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v) if v is not None else None,
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }

# =====================================================
# MODELO: Documento de Referencia
# =====================================================

class ReferenceDocument(BaseModel):
    """Modelo de documento de referencia"""
    id: Optional[str] = None
    nombre_archivo: str = Field(..., min_length=1, max_length=255)
    contenido_extraido: str
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    activo: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# =====================================================
# MODELOS DE ENTRADA PARA FORMULARIOS
# =====================================================

class IndicatorInputData(BaseModel):
    """Datos de entrada para cálculo de indicadores"""
    # Para ARR
    recaidas: Optional[int] = Field(None, ge=0)
    
    # Para lesiones RM
    lesiones_t1_gd: Optional[int] = Field(None, ge=0)
    lesiones_t2_actuales: Optional[int] = Field(None, ge=0)
    lesiones_t2_previas: Optional[int] = Field(None, ge=0)
    
    # Para EDSS
    edss_actual: Optional[Decimal] = Field(None, ge=0, le=10)
    edss_basal: Optional[Decimal] = Field(None, ge=0, le=10)
    
    @validator('edss_actual', 'edss_basal')
    def validar_edss(cls, v):
        """Valida que EDSS sea múltiplo de 0.5"""
        if v is not None and float(v) % 0.5 != 0:
            raise ValueError('EDSS debe ser múltiplo de 0.5')
        return v
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v) if v is not None else None
        }
