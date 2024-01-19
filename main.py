from fastapi import FastAPI, Depends, HTTPException, Request



from sqlalchemy.orm import Session

from app.config.jwt import generate_jwt, decode_jwt
from app.controllers.user_controller import user_router
from app.database.db import get_db, User

app = FastAPI()


@app.get("/")
async def root(db: Session = Depends(get_db)):
    return "Hello Fast API"


# Include the router in the main FastAPI app
app.include_router(user_router)