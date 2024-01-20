from fastapi import FastAPI
from app.api.auth.views import router as route_auth

app = FastAPI()

app.include_router(route_auth)
