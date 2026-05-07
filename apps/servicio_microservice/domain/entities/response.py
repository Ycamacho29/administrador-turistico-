'''response.py'''

from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Any, List, Dict
import time

T = TypeVar('T')


@dataclass
class Paginacion:
    pagina_actual: int
    total_paginas: int
    total_elementos: int
    elementos_por_pagina: int
    primera_pagina: bool
    ultima_pagina: bool


@dataclass
class ErrorDetalle:
    campo: Optional[str] = None
    codigo_error: Optional[str] = None
    mensaje: Optional[str] = None
    valor_rechazado: Optional[str] = None
    ubicacion: Optional[str] = None
    stack_trace: Optional[str] = None


@dataclass
class ResponseDTO(Generic[T]):
    estatus: str
    codigo: Optional[str] = None
    mensaje: Optional[str] = None
    mensaje_tecnico: Optional[str] = None
    data: Optional[T] = None
    paginacion: Optional[Paginacion] = None
    errores: List[ErrorDetalle] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: int = field(default_factory=lambda: int(time.time() * 1000))

    @classmethod
    def success(cls, data: Optional[T] = None, mensaje: Optional[str] = None) -> 'ResponseDTO[T]':
        return cls(estatus="success", data=data, mensaje=mensaje)

    @classmethod
    def error(cls, mensaje: str, errores: Optional[T] = None) -> 'ResponseDTO[T]':
        return cls(estatus="error", mensaje=mensaje, errores=errores)
