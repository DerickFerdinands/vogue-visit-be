from fastapi import FastAPI, Depends, HTTPException, Request



from sqlalchemy.orm import Session

from app.config.jwt import generate_jwt, decode_jwt
from app.controllers.salon_controller import salon_router
from app.controllers.service_controller import service_router
from app.controllers.user_controller import user_router
from app.database.db import get_db, User

app = FastAPI()


@app.get("/")
async def root(db: Session = Depends(get_db)):
    return "Hello Fast API"


# Include the router in the main FastAPI app
app.include_router(user_router)
app.include_router(salon_router)
app.include_router(service_router)