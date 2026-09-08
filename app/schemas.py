from pydantic import BaseModel, Field
from typing import List

class ImageMetadataSchema(BaseModel):
    subject: str = Field(..., description="Main subject of the image (e.g. red fox)")
    category: str = Field(..., description="High level category (e.g. animal)")
    attributes: List[str] = Field(default_factory=list, description="Visual traits (e.g. orange fur, forest)")
    caption: str = Field(..., description="Detailed description of the image")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence score between 0 and 1")

class RejectResponse(BaseModel):
    status: str = "REJECTED"
    reason: str