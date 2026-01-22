from fastapi import FastAPI
from app.api.data_ingestion.controller import router as upload_router

app = FastAPI(title="File Upload API")

app.include_router(upload_router)
