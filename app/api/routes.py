from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.models.project import ProjectDescriptionEnhencementRequest, ExperienceEnhencementRequest
from app.services import utils

router = APIRouter()

# to enhance project description
@router.post("/project")
async def enhance_project_description(request: ProjectDescriptionEnhencementRequest):
    enhanced = utils.enhance_project_description_with_gemini(request.description)
    return {"enhanced_description": enhanced}

# to enhence experience
@router.post("/experience")
async def enhance_experience_description(request: ExperienceEnhencementRequest):
    enhanced = utils.enhance_Work_experience_with_gemini(request.description)
    return {"enhanced_work_experience": enhanced}

# it will generate all resume and send in zip file
@router.post("/generate-resume-zip/")
async def generate_resume_zip(data: dict):
    zip_path = utils.generate_all_templates_and_zip(data)
    return FileResponse(zip_path, filename="resumes.zip", media_type="application/zip")

# to generate resume based on the user selected template
@router.post("/generate-resume/")
async def generate_resume(data: dict):
    pdf_path = utils.generate_resume_from_template(data)
    return FileResponse(pdf_path, filename="resume.pdf", media_type="application/pdf")
