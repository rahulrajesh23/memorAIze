from pydantic import BaseModel
from typing import List, Optional

class QuestionAndDocumentsRequest(BaseModel):
    question: str
    documents: List[str]

class GetQuestionAndFactsResponse(BaseModel):
    question: str
    facts: Optional[List[str]] = None
    status: str