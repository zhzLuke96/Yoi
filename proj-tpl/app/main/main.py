# --
# main package entry point
# --

from .yoi.application import Application
from .views import views_router

__all__ = ("app",)
app = Application(router=views_router)
