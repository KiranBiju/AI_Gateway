from fastapi import FastAPI
from db.database import engine
from services import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def head_root():
    return {"system is running"}
