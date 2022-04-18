from uuid import uuid4
from fastapi import APIRouter, File, UploadFile 
from app.config.settings import settings
from app.scripts.manage import Manage

import os, shutil

router = APIRouter(
    tags=['upload'],
    prefix="/upload"
)

@router.post('/')
async def run_pipeline(files: list[UploadFile] = File(...)):  
    # generate id per submission (for group or single file)
    file_id = str(uuid4())
    uploads_dir = "{}/{}".format(settings.UPLOADS, file_id)
    result_dir = "{}/{}".format(settings.RESULTS, file_id)
    os.mkdir(uploads_dir)
    os.mkdir(result_dir)

    jobs = []
    
    for file in files: 
        filename_split = file.filename.split(".")
        filename = filename_split[0]
        file_extensions = filename_split[1:]
        file_type = file_extensions[0] 
        file_dir = "{}/{}".format(uploads_dir, file.filename)
        job = {'filename' : filename, 'input_type': file_type, 'inp': file_dir}
        jobs.append(job)

        with open(file_dir, "wb+") as f:
                shutil.copyfileobj(file.file, f)

    manage = Manage(jobs, uploads_dir,result_dir, 5)
    data = await manage.run()
    d3_data = data.to_json(orient='index')
    
    return d3_data
        
    
