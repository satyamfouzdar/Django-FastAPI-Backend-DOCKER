import os
from django.apps import apps
from django.conf import settings
from django.core.wsgi import get_wsgi_application

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

apps.populate(settings.INSTALLED_APPS)


from core.api_router import router as api_router

application = get_wsgi_application()


def get_application() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json", debug=settings.DEBUG)
    # Set all CORS enabled origins
    app.add_middleware(CORSMiddleware, allow_origins = [str(origin) for origin in settings.ALLOWED_HOSTS] or ["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

	# Include all api endpoints
    app.include_router(api_router, prefix=settings.API_V1_STR)

	# Mounts an independent web URL for Django WSGI application
    app.mount(f"{settings.WSGI_APP_URL}", WSGIMiddleware(application))

    # Set Up the static files and directory to serve django static files
    app.mount("/static", StaticFiles(directory="static"), name="static")

    return app

app = get_application()
