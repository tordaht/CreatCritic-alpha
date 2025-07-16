"""
CreaCritic - Konfigürasyon Modülü
Seri No: CR-012-v1.0
"""

__version__ = "1.0.0"
__serial_no__ = "CR-012-v1.0"

from .settings import *
from .credentials import validate_credentials

__all__ = [
    'validate_credentials'
] 