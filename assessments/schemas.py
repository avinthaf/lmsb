from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional

@dataclass
class CreateAssessmentInput:
    school_id: str
    name: str

@dataclass
class Assessment:
    id: UUID
    school_id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    description: Optional[str] = None

@dataclass
class AssessmentQuestion:
    id: UUID
    school_id: UUID
    category_id: UUID
    text: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

@dataclass
class AssessmentsAssessmentQuestion:
    id: UUID
    assessment_id: UUID
    assessment_question_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

@dataclass
class AssessmentQuestionAnswerType:
    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

@dataclass
class AssessmentQuestionAnswer:
    id: UUID
    assessment_question_answer_type_id: UUID
    assessment_question_id: UUID
    label: str
    text: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
