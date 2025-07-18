from pydantic import BaseModel

class ProjectDescriptionEnhencementRequest(BaseModel):
    description: str

class ExperienceEnhencementRequest(BaseModel):
    description: str