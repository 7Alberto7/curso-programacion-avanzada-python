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