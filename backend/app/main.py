from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import uploads
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(uploads.router)

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return RedirectResponse(url='/docs')

