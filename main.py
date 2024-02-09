from fastapi import FastAPI, Depends, HTTPException, Request



from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from app.config.jwt import generate_jwt, decode_jwt
from app.controllers.appointment_controller import appointment_router
from app.controllers.payment_controller import payment_router
from app.controllers.paypal_controller import paypal_router
from app.controllers.salon_controller import salon_router
from app.controllers.service_controller import service_router
from app.controllers.time_slot_controller import time_slot_router
from app.controllers.user_controller import user_router
from app.database.db import get_db, User

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root(db: Session = Depends(get_db)):
    return "Hello Fast API"


# Include the router in the main FastAPI app
app.include_router(user_router)
app.include_router(salon_router)
app.include_router(service_router)
app.include_router(time_slot_router)
app.include_router(appointment_router)
app.include_router(payment_router)
app.include_router(paypal_router)
