from pydantic import BaseModel
from typing import Optional, List, Dict

class BusinessProfile(BaseModel):
    name: str = "رنة جرس"
    url: str = "https://axssor.com/"
    category: str = "Fashion accessories store"
    description: str = "متجر رنة جرس لإكسسوارات الموضة"
    address: str = "Saudi Arabia"
    phone: str = "055 484 0091"
    
class AnalysisResult(BaseModel):
    score: float
    phase: str
    confidence: float
    recommendations: List[str]
    explanation: str
