from uuid import uuid4
from fastapi import APIRouter, File, UploadFile 
from app.config.settings import settings
from app.scripts.process import Process

import os, shutil

router = APIRouter(
    tags=['upload'],
    prefix="/upload"
)

@router.post('/')
async def run_pipeline(files: list[UploadFile] = File(...)):  
    file_id_lst = []
    for file in files: 
        file_extensions = file.filename.split(".")[1:]
        file_type = file_extensions[0]
        file_id = str(uuid4())
        file_location = "{}/{}".format(settings.UPLOADS, file_id)
        result_dir = "{}/{}".format(settings.RESULTS, file_id)

        os.mkdir(file_location)
        os.mkdir(result_dir)

        file_dir = "{}/{}".format(file_location, file.filename)
        with open(file_dir, "wb+") as f:
                shutil.copyfileobj(file.file, f)
        file_id_lst.append(file_id)

        process = Process(file_dir,result_dir, file_type)

        result = await process.run()
        shutil.rmtree(file_location)
        
    
    return {'result': file.filename}
        
    
