"""Archivo __init__.py para el paquete ai"""
from .deepseek_client import DeepSeekClient
from .copilot_client import CopilotClient
from .prompt_builder import MedicalPromptBuilder
from .dual_consultation import DualAIConsultation

__all__ = [
    'DeepSeekClient',
    'CopilotClient',
    'MedicalPromptBuilder',
    'DualAIConsultation'
]
