
# app/modelos.py
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from functools import wraps
from datetime import datetime
from typing import Any, Callable

def con_logging(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        ts = datetime.now().isoformat(timespec="seconds")
        who = getattr(self, "email", "desconocido")
        print(f"[{ts}] [{self.__class__.__name__}] <{who}> INICIO: {func.__name__}")
        res = func(self, *args, **kwargs)
        print(f"[{ts}] [{self.__class__.__name__}] <{who}> FIN: {func.__name__}")
        return res
    return wrapper



class NotificadorMixin:
    def enviar_email(self, asunto: str, cuerpo: str) -> None:
        print(f"[EMAIL a {self.email}] {asunto}: {cuerpo}")

    def activar(self):
        self.enviar_email('activado','babababa')

class LoggerMixin:
    """Mixin de logging simple. Supone que la clase hija tiene .email y .__class__.__name__."""
    
    def log_evento(self, msg: str, **context: Any) -> None:
        ts = datetime.now().isoformat(timespec="seconds")
        who = getattr(self, "email", "desconocido")
        extra = f" {context}" if context else ""
        print(f"[{ts}] [{self.__class__.__name__}] <{who}> {msg}{extra}")

    # # Ejemplo de método que coopera con super() para cadenas MRO
    def activar(self) -> None:
        self.log_evento("Activando usuario…")
        super().activar()  # delega al siguiente en el MRO
        self.log_evento("Usuario activado")


def notificador():
    """
    Decorador de clase que:
      1) Inyecta ControllerMixin por herencia.
      2) Fija base_path en la clase resultante.
    """
    def _decorar(cls):

        nombre = cls.__name__
        attrs = dict(cls.__dict__)
        # Limpiezas opcionales para evitar warnings en type()
        attrs.pop("__dict__", None)
        attrs.pop("__weakref__", None)

        Nueva = type(nombre, (NotificadorMixin, cls), attrs)
        return Nueva
    return _decorar




def factory():
    """
    Decorador de clase que:
      1) Inyecta ControllerMixin por herencia.
      2) Fija base_path en la clase resultante.
    """
    def _decorar(cls):


        cls.Factory = []
       

        return cls
    return _decorar



def logger():
    """
    Decorador de clase que:
      1) Inyecta ControllerMixin por herencia.
      2) Fija base_path en la clase resultante.
    """
    def _decorar(cls):

        nombre = cls.__name__
        attrs = dict(cls.__dict__)
        # Limpiezas opcionales para evitar warnings en type()
        attrs.pop("__dict__", None)
        attrs.pop("__weakref__", None)

        Nueva = type(nombre, (LoggerMixin, cls), attrs)
        return Nueva
    return _decorar


# --- Base abstracta ---
class BaseUsuario(ABC):
    @abstractmethod
    def permisos(self) -> list[str]:
        """Lista de permisos concedidos al usuario."""
        ...

    def tiene_permiso(self, permiso: str) -> bool:
        return permiso in self.permisos()

# --- Usuario (de Fase 2) HEREDA de BaseUsuario ---
# @logger()
# @notificador()
class Usuario(BaseUsuario):
    contador = 0
    ROLES_VALIDOS = {"usuario", "admin", "invitado"}

    def __init__(self, nombre: str, email: str, rol: str = "usuario", activo: bool = True):
        self.nombre = nombre
        self._email: str | None = None
        self.email = email
        self._rol: str | None = None
        self.rol = rol
        self.activo = activo
        self.__password_hash: str | None = None
        Usuario.contador += 1

    # Representación
    def presentarse(self) -> str:
        return f"Soy {self.nombre} ({self.email})"


    @con_logging
    def activar(self) -> None: self.activo = True


    def desactivar(self) -> None: self.activo = False

    def __str__(self) -> str:
        estado = "activo" if self.activo else "inactivo"
        return f"{self.nombre} <{self.email}> ({self.rol}) [{estado}]"

    def __repr__(self) -> str:
        return (f"Usuario(nombre={self.nombre!r}, email={self.email!r}, "
                f"rol={self.rol!r}, activo={self.activo!r})")

    # Email
    @property
    def email(self) -> str:
        return self._email or ""

    @email.setter
    def email(self, value: str) -> None:
        v = (value or "").strip().lower()
        if "@" not in v or v.startswith("@") or v.endswith("@"):
            raise ValueError(f"Email inválido: {value!r}")
        self._email = v

    # Rol
    @property
    def rol(self) -> str:
        return self._rol or "usuario"

    @rol.setter
    def rol(self, value: str) -> None:
        v = (value or "").strip().lower()
        if v not in self.ROLES_VALIDOS:
            raise ValueError(f"Rol inválido: {value!r}. Válidos: {sorted(self.ROLES_VALIDOS)}")
        self._rol = v

    # Password (demo)
    def set_password(self, p: str) -> None:
        if not p or len(p) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        self.__password_hash = f"hash::{p}"

    def check_password(self, p: str) -> bool:
        return self.__password_hash == f"hash::{p}"

    @classmethod
    def desde_dict(cls, datos: dict) -> "Usuario":
        return cls(
            nombre=datos.get("nombre", ""),
            email=datos.get("email", ""),
            rol=datos.get("rol", "usuario"),
            activo=bool(datos.get("activo", True)),
        )

    # Permisos por defecto del rol "usuario"
    def permisos(self) -> list[str]:
        return ["ver"]


class Admin(Usuario):
    def __init__(self, nombre: str, email: str, activo: bool = True):
        super().__init__(nombre, email, rol="admin", activo=activo)

    def permisos(self) -> list[str]:
        return ["ver", "crear", "editar", "borrar"]

    # ✅ NUEVO: extender sin duplicar
    def presentarse(self) -> str:
        base = super().presentarse()   # "Soy {nombre} ({email})"
        return f"[ADMIN] {base}"


# @logger()
class Moderador(Usuario):
    def __init__(self, nombre: str, email: str, nivel: int = 1, activo: bool = True):
        super().__init__(nombre, email, rol="moderador", activo=activo)

        if not isinstance(nivel, int) or nivel < 1:
            raise ValueError("El nivel de moderador debe ser un entero >= 1")


        self.nivel = nivel

    def permisos(self) -> list[str]:
        super().permisos()
        base = ["ver", "editar"]
        if self.nivel >= 2:
            base.append("borrar")
        return base

    def ascender(self) -> list[str]:
        self.nivel += 1
        return self.permisos()

    # ✅ REESCRITO: aprovechar el __str__ del padre
    def __str__(self) -> str:
        return f"[MODERADOR-N{self.nivel}] {super().__str__()}"

    @classmethod
    def basico(cls, nombre: str, email: str) -> "Moderador":
        return cls(nombre, email, nivel=1)

    @classmethod
    def avanzado(cls, nombre: str, email: str) -> "Moderador":
        return cls(nombre, email, nivel=2)










# class AdminConLogger(LoggerMixin, Admin):
#     """Admin con capacidades de logging vía mixin."""
#     # hereda todo; si quieres, puedes extender presentarse/activar usando super()
#     def presentarse(self) -> str:
#         base = super().presentarse()
#         self.log_evento("presentarse() invocado")
#         return base


# Moderador

class AuditoriaMixin:
    def __init__(self, nombre: str, email: str, activo: bool = True):
        self._audit = []
        super().__init__(nombre, email, activo=activo)

    def auditar(self, evento: str):
        self._audit.append(evento)

    def observar(selt):
        print(selt._audit)



# class AdminFull(NotificadorMixin, LoggerMixin, Admin):
#     pass


# class ModeradorNotificador(NotificadorMixin,Moderador):
#     pass


# class AdminAuditoria(AuditoriaMixin, Admin):
#     pass


