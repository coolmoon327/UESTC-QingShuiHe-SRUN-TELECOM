from .common import AutoLogin as BaseAutoLogin

try:
    from .browser import AutoLogin as BrowserAutoLogin
except ModuleNotFoundError:
    pass

from .request import AutoLogin as RequestAutoLogin

__all__ = ["BrowserAutoLogin", "RequestAutoLogin", "BaseAutoLogin"]
