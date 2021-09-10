from aiohttp import web

from .views import ROUTES

__all__ = (
    'create_app',
)


async def create_app() -> web.Application:
    app = web.Application()
    app.router.add_routes(ROUTES)
    return app
