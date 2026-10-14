from pydantic import BaseModel, Field

from api.models import Category, Severity


class TriageResult(BaseModel):
    category: Category
    severity: Severity
    confidence: float = Field(..., ge=0, le=1)