from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.config import settings
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.core import read_json

words = read_json.ReadJson()

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.mount("/static", StaticFiles(directory="statics"), name="static")

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/", response_class=RedirectResponse)
async def to_home():
    """
    this method redirect / url to /api/v1/home
    :return: redirect to new url
    """
    return RedirectResponse(url=words.read_home_url())

app.include_router(api_router, prefix=settings.API_V1_STR)

