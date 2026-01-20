from fastapi import FastAPI
from app.api.controller import router as upload_router

app = FastAPI(title="File Upload API")

app.include_router(upload_router)
