# --
# views
# --

from .yoi.router import Router

__all__ = ("views_router",)

views_router = Router()

views_router.add_static_folder("/", "./www/")


@views_router(r"/?$", methods=["GET"])
async def HelloWorld():
    return "<h1>hello yoi~</h1>"
