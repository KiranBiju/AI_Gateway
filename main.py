from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def head_root():
    return {"system is running"}
