from fastapi import FastAPI
from app.db.database import engine
from app.db import models
from app.api.routes import auth
from app.schemas.users import UserCreate, UserLogin
from app.api.routes import api_keys

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)

app.include_router(api_keys.router)

@app.get("/")
async def head_root():
    return {"status": "system is running"}

@app.post("/signup")
def signup(user: UserCreate):
    return {
        "email": user.email,
        "message": "User created"
    }


@app.post("/login")
def login(user: UserLogin):
    return {
        "email": user.email,
        "message": "Login request received"
    }