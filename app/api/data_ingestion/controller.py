from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.config import UPLOAD_DIR
from app.api.service.file_store import save_uploaded_file

router = APIRouter(prefix="/files", tags=["File Upload"])

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    saved_path = save_uploaded_file(UPLOAD_DIR, file)

    return {
        "original_filename": file.filename,
        "stored_filename": saved_path.name,
        "stored_path": str(saved_path)
    }
