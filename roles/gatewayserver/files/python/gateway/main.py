from pathlib import Path

import aiohttp_jinja2
import aiohttp_session
import jinja2
from aiohttp import web
# from aiohttp_session.cookie_storage import EncryptedCookieStorage

# from .db import prepare_database
from .settings import Settings
from .views import index, Alive, Images, InstallConfig, Imaging

THIS_DIR = Path(__file__).parent


async def startup(app: web.Application):
    settings: Settings = app['settings']


async def cleanup(app: web.Application):
    pass

def create_app():
    app = web.Application()
    settings = Settings()
    app.update(
        settings=settings,
        static_root_url='/static/',
    )

    jinja2_loader = jinja2.FileSystemLoader(str(THIS_DIR / 'templates'))
    aiohttp_jinja2.setup(app, loader=jinja2_loader)

    app.on_startup.append(startup)
    app.on_cleanup.append(cleanup)

    # aiohttp_session.setup(app, EncryptedCookieStorage(settings.auth_key, cookie_name=settings.cookie_name))

    # import pdb; pdb.set_trace()
    app.router.add_static('/static', str(THIS_DIR / 'static'))

    app.router.add_get('/', index, name='index')
    app.router.add_view('/alive', Alive, name='Alive')

    app.router.add_view('/images', Images, name='ImagesIndex')
    app.router.add_view('/images/{file_name}', Images, name='Images')
    
    app.router.add_view('/config/{name}', InstallConfig, name="Config")

    app.router.add_view('/imaging/', InstallConfig, name="ImagingIndex")
    app.router.add_view('/imaging/{name}', InstallConfig, name="Imaging")

    for resource in app.router.resources():
        print(resource)

    return app