from fastapi import APIRouter, File, UploadFile

router = APIRouter(
    tags=['uploads']
)

@router.post('/')
async def create_upload(
    files: list[UploadFile] = File(...)
):
    return {"filenames": [file.filename for file in files]}
