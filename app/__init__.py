from fastapi import FastAPI
from app.api.auth.views import router as route_auth
from app.api.bulletin.views import router as route_bulletin
from app.api.users.views import router as user_route

app = FastAPI()

app.include_router(route_auth)
app.include_router(route_bulletin)
app.include_router(user_route)
