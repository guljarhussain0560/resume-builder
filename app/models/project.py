from pydantic import BaseModel

class ProjectDescriptionRequest(BaseModel):
    description: str

class EnhancedDescriptionResponse(BaseModel):
    enhanced_description: str
