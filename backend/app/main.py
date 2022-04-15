from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import uploads

app = FastAPI()

app.include_router(uploads.router)

@app.get("/")
async def root():
    return RedirectResponse(url='/docs')

