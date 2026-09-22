from fastapi import FastAPI

app = FastAPI(title="Video Hosting API")

@app.get("/")
async def root():
    return {"message": "Hello World"}

