'''request.py'''

from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Any, Dict
import time

T = TypeVar('T')


@dataclass
class Metadata:
    version_api: Optional[str] = None
    dispositivo: Optional[str] = None
    sistema_operativo: Optional[str] = None
    aplicacion: Optional[str] = None
    uuid_transaccion: Optional[str] = None
    timestamp: int = field(default_factory=lambda: int(time.time() * 1000))
    usuario: Optional[str] = None
    ip_origen: Optional[str] = None
    session_id: Optional[str] = None
    user_agent: Optional[str] = None


@dataclass
class RequestDTO(Generic[T]):
    metadata: Optional[Metadata] = None
    data: Optional[T] = None
    parametros: Dict[str, Any] = field(default_factory=dict)
    token: Optional[str] = None
    idioma: Optional[str] = None
    debug: bool = False

    @classmethod
    def of(cls, data: T, usuario: Optional[str] = None) -> 'RequestDTO[T]':
        """Replica el método static of() de Java"""
        metadata = Metadata(usuario=usuario) if usuario else None
        return cls(data=data, metadata=metadata)
