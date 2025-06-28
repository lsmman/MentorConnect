from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import auth, users, mentors, match_requests, images, profile
from app.core.config import settings
from app.core.error_handler import ErrorHandlerMiddleware
import os

app = FastAPI(title="MentorConnect API", docs_url="/swagger-ui", openapi_url="/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(mentors.router, prefix="/api")
app.include_router(match_requests.router, prefix="/api")
app.include_router(images.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(match_requests.router)
app.include_router(images.router)

# static 폴더 서빙 (openapi.yaml 포함)
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# /v3/api-docs에서 openapi.yaml 반환
@app.get("/v3/api-docs", include_in_schema=False)
def get_openapi_yaml():
    yaml_path = os.path.join(os.path.dirname(__file__), "static", "openapi.yaml")
    return FileResponse(yaml_path, media_type="application/yaml")

app.add_middleware(ErrorHandlerMiddleware)

# DB seed: python app/db/seed.py

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/swagger-ui")
