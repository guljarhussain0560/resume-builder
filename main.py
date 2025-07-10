from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from utils import generate_all_templates_and_zip

app = FastAPI()

@app.post("/generate-resume-zip/")
async def generate_resume_zip(data: dict = Body(...)):
    zip_path = generate_all_templates_and_zip(data)
    return FileResponse(zip_path, filename="resumes.zip", media_type="application/zip")
