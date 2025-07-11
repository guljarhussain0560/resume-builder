from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from utils import generate_all_templates_and_zip, generate_resume_from_template

app = FastAPI()

@app.post("/generate-resume-zip/")
async def generate_resume_zip(data: dict = Body(...)):
    zip_path = generate_all_templates_and_zip(data)
    return FileResponse(zip_path, filename="resumes.zip", media_type="application/zip")

# API for resume generation according to the user template selection.
@app.post("/generate-resume/")
async def generate_resume(data: dict = Body(...)):
    pdf_path = generate_resume_from_template(data)
    return FileResponse(pdf_path, filename="resume.pdf", media_type="application/pdf")