from fastapi import FastAPI
from routers import solicitation, user, vehicle

app = FastAPI()

app.include_router(user.router)
app.include_router(solicitation.router)
app.include_router(vehicle.router)